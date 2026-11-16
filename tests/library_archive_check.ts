/**
 * Behavioural checks for the archive layer, run against a FAKE kiwix-serve built from the
 * documented endpoints. This proves the adapter does what it claims against that model; it does
 * not prove the model matches every kiwix-serve release. Use tools/kiwix_smoke.ts for that.
 *
 * Prints {"passed": n, "failures": [...]} and exits non-zero on any failure.
 */
import {
  ARCHIVE_DEFAULT_TRUST, ArchiveError, KiwixServeSource, archiveEntryId, archiveRoutes, decodeEntities,
  encodeArchivePath, findInArchive, htmlToText, isLoopbackHost, parseArchiveEntryId, promoteToNode,
} from "../core/library/archive/index";
import type { CultureEmbedding, NuanceParameters } from "../core/library/types";

declare const require: (name: string) => any;
declare const process: { exit: (code: number) => void };

const http = require("http");
const failures: string[] = [];
let passed = 0;

async function check(name: string, fn: () => void | Promise<void>): Promise<void> {
  try { await fn(); passed++; } catch (e) { failures.push(`${name}: ${(e as Error).message}`); }
}
function eq(a: unknown, b: unknown, what = ""): void {
  if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(`${what} expected ${JSON.stringify(b)}, got ${JSON.stringify(a)}`);
}
function ok(cond: boolean, what: string): void { if (!cond) throw new Error(what); }
async function rejects(p: Promise<unknown>, match: RegExp | null = null): Promise<ArchiveError> {
  try { await p; } catch (e) {
    ok(e instanceof ArchiveError, `expected ArchiveError, got ${(e as Error).name}`);
    if (match) ok(match.test((e as Error).message), `message ${JSON.stringify((e as Error).message)} !~ ${match}`);
    return e as ArchiveError;
  }
  throw new Error("expected rejection");
}

// ---------------------------------------------------------------- fake kiwix-serve
const seen: string[] = [];
let failSearch = false;
let failSuggest = false;
const BIG = "<html><body>" + "x".repeat(5000) + "</body></html>";

const server = http.createServer((req: any, res: any) => {
  const url = new URL(req.url, "http://127.0.0.1");
  seen.push(req.url);
  const send = (status: number, type: string, body: string | Uint8Array) => {
    res.writeHead(status, { "content-type": type });
    res.end(body);
  };
  if (url.pathname === "/catalog/v2/entries") {
    return send(200, "application/atom+xml", `<?xml version="1.0"?><feed>
      <entry><title>Wikipedia &amp; friends</title><language>eng</language><articleCount>6000000</articleCount>
        <link rel="x" type="application/x-zim" href="http://h/catalog/v2/illustration/abc"/>
        <link type="text/html" href="/content/wiki_en_2024-01"/></entry>
      <entry><title>No content link</title></entry>
      <entry><title>Bad name</title><link type="text/html" href="/content/has space"/></entry>
    </feed>`);
  }
  if (url.pathname === "/suggest") {
    if (failSuggest) return send(500, "text/plain", "boom");
    ok(url.searchParams.get("content") === "wiki_en_2024-01", "suggest content param");
    return send(200, "application/json", JSON.stringify([
      { value: "Fermi gas", label: "<b>Fermi</b> gas", kind: "path", path: "A/Fermi_gas" },
      { value: "Fermi level", label: "Fermi level", kind: "path", path: "A/Fermi_level" },
      { value: "containing 'Fermi'...", label: "containing 'Fermi'...", kind: "pattern" },
    ]));
  }
  if (url.pathname === "/search") {
    if (failSearch) return send(500, "text/plain", "no index");
    ok(url.searchParams.get("format") === "xml", "search format=xml");
    return send(200, "application/rss+xml", `<?xml version="1.0"?><rss><channel>
      <item><title>Fermi gas</title><link>/content/wiki_en_2024-01/A/Fermi_gas</link>
        <description>An ideal Fermi gas &amp; its states</description></item>
      <item><title>Café</title><link>http://127.0.0.1:1/content/wiki_en_2024-01/A/Caf%C3%A9?x=1</link>
        <description><![CDATA[<b>bold</b> snippet]]></description></item>
      <item><title>Other book</title><link>/content/other_book/A/Nope</link><description>x</description></item>
    </channel></rss>`);
  }
  if (url.pathname.startsWith("/content/wiki_en_2024-01/")) {
    const p = decodeURIComponent(url.pathname.slice("/content/wiki_en_2024-01/".length));
    if (p === "A/Fermi_gas") {
      return send(200, "text/html; charset=utf-8", `<!DOCTYPE html><html><head><title>Fermi gas &amp; sea</title>
        <style>p{color:red}</style><script>alert(1)</script></head><body><h1>Fermi gas</h1>
        <p>An ideal gas of fermions.<br>Second&nbsp;line &#955; &#x3bb; &#0; &#xD800; &amp;lt; end.</p>
        <!-- hidden --><ul><li>one</li><li>two</li></ul></body></html>`);
    }
    if (p === "A/Big") return send(200, "text/html", BIG);
    if (p === "I/logo.png") return send(200, "image/png", new Uint8Array([137, 80, 78, 71]));
    if (p === "A/Slow") { setTimeout(() => send(200, "text/html", "<p>late</p>"), 400); return; }
    return send(404, "text/plain", "not found");
  }
  send(404, "text/plain", "unknown");
});

const culture: CultureEmbedding = {
  origin: "test", languages: ["English"], contextuality: 0.5, indirectness: 0.5, collectivism: 0.5,
  timeOrientation: "present", powerDistance: 0.5, uncertaintyTolerance: 0.5, spiritualDimension: false, iconography: [],
};
const nuance: NuanceParameters = {
  abstractionLevel: 0.5, temporalScope: "generational", systemicDepth: 0.5, uncertaintyMargin: 0.5, applicabilityRadius: 0.5,
  ethicalDimension: [], counterExamples: [], relatedConcepts: [], updateFrequency: "static", relevanceToPAN: 0.5,
};

async function main(): Promise<void> {
  await new Promise<void>((r) => server.listen(0, "127.0.0.1", () => r()));
  const base = `http://127.0.0.1:${server.address().port}`;
  const src = new KiwixServeSource({ baseUrl: base });
  const BOOK = "wiki_en_2024-01";

  // ----- host and input guards
  await check("loopback hosts", () => {
    for (const h of ["localhost", "127.0.0.1", "127.9.9.9", "::1", "[::1]"]) ok(isLoopbackHost(h), h);
    for (const h of ["example.com", "10.0.0.5", "192.168.1.2", "127.0.0.1.evil.com", "0.0.0.0", "127.0.0.256"]) ok(!isLoopbackHost(h), h);
  });
  await check("constructor refuses remote, credentials, non-http", () => {
    for (const u of ["http://example.com:8080", "http://10.0.0.5", "http://127.0.0.1.evil.com"]) {
      let threw = false; try { new KiwixServeSource({ baseUrl: u }); } catch { threw = true; }
      ok(threw, u);
    }
    for (const u of ["http://user:pw@127.0.0.1:8080", "ftp://127.0.0.1", "not a url"]) {
      let threw = false; try { new KiwixServeSource({ baseUrl: u, allowRemote: true }); } catch { threw = true; }
      ok(threw, u);
    }
    new KiwixServeSource({ baseUrl: "http://example.com", allowRemote: true });
    new KiwixServeSource({ baseUrl: "http://[::1]:8080" });
    new KiwixServeSource();
  });
  await check("book names and paths are validated before any request", async () => {
    const before = seen.length;
    for (const b of ["../etc", "a b", "", "a/b", "x".repeat(201)]) await rejects(src.suggest(b, "x"), /invalid book/);
    for (const p of ["", "../x", "A/../B", "A//B", "A/./B", "A\u0000B"]) await rejects(src.getArticle(BOOK, p), /invalid archive path/);
    eq(seen.length, before, "no requests sent");
    eq(encodeArchivePath("A/Café &x"), "A/Caf%C3%A9%20%26x");
  });

  // ----- catalog, suggest, search
  await check("listBooks parses OPDS, skips entries without a usable content link", async () => {
    eq(await src.listBooks(), [{ name: BOOK, title: "Wikipedia & friends", language: "eng", articleCount: 6000000 }]);
  });
  await check("suggest strips markup, skips pseudo-suggestions, encodes the term", async () => {
    seen.length = 0;
    const hits = await src.suggest(BOOK, "Fermi gas & sea", 5);
    eq(hits.map((h) => h.id), [`kiwix:${BOOK}:A/Fermi_gas`, `kiwix:${BOOK}:A/Fermi_level`]);
    eq(hits[0].title, "Fermi gas");
    ok(seen[0].includes("term=Fermi%20gas%20%26%20sea") && seen[0].includes("count=5"), seen[0]);
    eq(await src.suggest(BOOK, "   "), []);
  });
  await check("search parses RSS, decodes entities and paths, ignores other books", async () => {
    const hits = await src.search(BOOK, "fermi");
    eq(hits.map((h) => h.path), ["A/Fermi_gas", "A/Café"]);
    eq(hits[0].snippet, "An ideal Fermi gas & its states");
    eq(hits[1].snippet, "bold snippet");
  });
  await check("limit is validated and clamped", async () => {
    await rejects(src.suggest(BOOK, "x", 0), /limit/);
    await rejects(src.search(BOOK, "x", 1.5), /limit/);
    seen.length = 0;
    await src.suggest(BOOK, "x", 5000);
    ok(seen[0].includes("count=100"), seen[0]);
  });

  // ----- articles
  await check("getArticle converts HTML to text", async () => {
    const a = await src.getArticle(BOOK, "A/Fermi_gas");
    eq(a.id, `kiwix:${BOOK}:A/Fermi_gas`);
    eq(a.title, "Fermi gas & sea");
    ok(!a.text.includes("alert") && !a.text.includes("color:red") && !a.text.includes("hidden"), "script/style/comment removed");
    ok(!/[<>]/.test(a.text.replace("&lt;", "")), "no tags left");
    ok(a.text.includes("An ideal gas of fermions.\nSecond line λ λ � � &lt; end."), JSON.stringify(a.text));
    ok(a.text.includes("one\ntwo"), "list items on separate lines");
    eq(a.truncated, false);
  });
  await check("getArticle truncates, rejects oversize, non-text and missing entries", async () => {
    const small = new KiwixServeSource({ baseUrl: base, maxTextChars: 100 });
    const t = await small.getArticle(BOOK, "A/Big");
    eq([t.text.length, t.truncated], [100, true]);
    await rejects(new KiwixServeSource({ baseUrl: base, maxArticleBytes: 1000 }).getArticle(BOOK, "A/Big"), /byte limit/);
    await rejects(src.getArticle(BOOK, "I/logo.png"), /not a text document/);
    const e = await rejects(src.getArticle(BOOK, "A/Missing"), /HTTP 404/);
    eq(e.status, 404);
  });
  await check("requests time out", async () => {
    const quick = new KiwixServeSource({ baseUrl: base, timeoutMs: 50 });
    await rejects(quick.getArticle(BOOK, "A/Slow"), /request failed/);
  });
  await check("a dead server yields ArchiveError, not a crash", async () => {
    await rejects(new KiwixServeSource({ baseUrl: "http://127.0.0.1:1", timeoutMs: 500 }).listBooks(), /request failed/);
  });

  // ----- bridge
  await check("findInArchive merges, de-duplicates, tolerates one failing endpoint", async () => {
    const hits = await findInArchive(src, BOOK, "fermi", 10);
    eq(hits.map((h) => h.path), ["A/Fermi_gas", "A/Fermi_level", "A/Café"]);
    eq(hits[0].snippet, "An ideal Fermi gas & its states", "snippet filled from full-text hit");
    failSearch = true;
    eq((await findInArchive(src, BOOK, "fermi", 10)).length, 2);
    failSearch = false; failSuggest = true;
    eq((await findInArchive(src, BOOK, "fermi", 10)).length, 2);
    failSearch = true;
    await rejects(findInArchive(src, BOOK, "fermi", 10), /HTTP 500/);
    failSearch = false; failSuggest = false;
    eq((await findInArchive(src, BOOK, "fermi", 1)).length, 1);
  });
  await check("promoteToNode requires caller-supplied culture/nuance and sets provenance", async () => {
    const article = await src.getArticle(BOOK, "A/Fermi_gas");
    const added: any[] = [];
    const sink = { addNode: (...args: any[]) => { const node: any = { id: args[0], provenance: { source: args[4].origin, verificationMethod: "x", verificationChain: ["z"] } }; added.push([args, node]); return node; } };
    const node = promoteToNode(sink as any, article, culture, nuance);
    eq(added[0][0].slice(0, 3), [article.id, "knowledge", "Fermi gas & sea"]);
    eq(added[0][0][6], ARCHIVE_DEFAULT_TRUST);
    eq(added[0][0][7], ["archive", BOOK]);
    eq([node.provenance.source, node.provenance.verificationMethod, node.provenance.verificationChain], [article.id, "community", []]);
    for (const bad of [-0.1, 1.1, NaN]) {
      let threw = false; try { promoteToNode(sink as any, article, culture, nuance, { trustWeight: bad }); } catch { threw = true; }
      ok(threw, `trust ${bad}`);
    }
    let threw = false; try { promoteToNode(sink as any, article, null as any, nuance); } catch { threw = true; }
    ok(threw, "culture required");
    threw = false; try { promoteToNode(sink as any, { ...article, text: "" }, culture, nuance); } catch { threw = true; }
    ok(threw, "empty article refused");
  });

  // ----- routes
  await check("routes map validation to 400, upstream failures to 502, success to 200", async () => {
    const r = archiveRoutes(src);
    eq((await r.books()).status, 200);
    eq((await r.suggest({ book: BOOK, term: "fermi" })).status, 200);
    eq((await r.suggest({ book: "../x", term: "a" })).status, 400);
    eq((await r.suggest({ book: BOOK })).status, 400);
    eq((await r.suggest({ book: BOOK, term: "a", limit: "0" })).status, 400);
    eq((await r.search({ book: BOOK })).status, 400);
    eq((await r.search({ book: BOOK, q: "fermi" })).status, 200);
    eq((await r.article({ book: BOOK, path: "../x" })).status, 400);
    eq((await r.article({ book: BOOK, path: "A/Fermi_gas" })).status, 200);
    const missing = await r.article({ book: BOOK, path: "A/Missing" });
    eq(missing.status, 502);
    ok(JSON.stringify(missing.body).includes("404"), "upstream status surfaced");
    const boom = archiveRoutes({ ...src, kind: "x", listBooks: () => { throw new TypeError("secret detail"); } } as any);
    const failed = await boom.books();
    eq([failed.status, JSON.stringify(failed.body).includes("secret")], [500, false]);
  });

  // ----- text helpers and ids
  await check("htmlToText and decodeEntities edge cases", () => {
    eq(decodeEntities("&amp;lt; &unknown; &#x110000; &#0;"), "&lt; &unknown; � �");
    const nested = htmlToText("<script>a<script>b</script>c</script>d");
    ok(!nested.includes("a") && !nested.includes("b") && !/[<>]/.test(nested), `script bodies must not leak: ${JSON.stringify(nested)}`);
    eq(htmlToText("a<br/>b<br>c"), "a\nb\nc");
    eq(htmlToText("  <p> x </p>\n\n\n\n<p>y</p>  "), "x\n\ny");
    eq(htmlToText("<div>unclosed <b>bold"), "unclosed bold");
  });
  await check("entry ids round-trip", () => {
    eq(archiveEntryId("b", "/A/x:y"), "kiwix:b:A/x:y");
    eq(parseArchiveEntryId("kiwix:b:A/x:y"), { book: "b", path: "A/x:y" });
    eq(parseArchiveEntryId("matter:element:H"), null);
  });

  server.close();
  console.log(JSON.stringify({ passed, failures }));
  process.exit(failures.length === 0 ? 0 : 1);
}

main();
