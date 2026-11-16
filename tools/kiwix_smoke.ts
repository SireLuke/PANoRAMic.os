/**
 * Smoke test for a REAL kiwix-serve. Run it against the server on your own machine to confirm
 * the archive adapter parses what your Kiwix version actually returns.
 *
 *   kiwix-serve --port 8080 your_file.zim
 *   (compile and run as described in core/library/ARCHIVE.md)
 *   node kiwix_smoke.js [baseUrl] [book] [query]
 *
 * It only talks to the URL you give it (loopback by default) and prints a short excerpt to your
 * terminal. If a step returns nothing it prints the start of the raw response, so a changed
 * response format is easy to report.
 */
import { DEFAULT_KIWIX_URL, KiwixServeSource } from "../core/library/archive/index";

declare const process: { argv: string[]; exit: (code: number) => void };

const baseUrl = process.argv[2] ?? DEFAULT_KIWIX_URL;
const bookArg = process.argv[3];
const query = process.argv[4] ?? "Fermi";

async function rawHead(path: string): Promise<string> {
  try {
    const res = await fetch(baseUrl.replace(/\/+$/, "") + path);
    return `HTTP ${res.status} ${res.headers.get("content-type")}\n${(await res.text()).slice(0, 400)}`;
  } catch (e) {
    return `request failed: ${(e as Error).message}`;
  }
}

async function main(): Promise<void> {
  const problems: string[] = [];
  const step = async <T>(name: string, fn: () => Promise<T>): Promise<T | null> => {
    try {
      const out = await fn();
      console.log(`ok    ${name}`);
      return out;
    } catch (e) {
      problems.push(name);
      console.log(`FAIL  ${name}: ${(e as Error).message}`);
      return null;
    }
  };

  let src: KiwixServeSource;
  try {
    src = new KiwixServeSource({ baseUrl });
  } catch (e) {
    console.log(`cannot use ${baseUrl}: ${(e as Error).message}`);
    process.exit(1);
    return;
  }
  const books = await step("list books", () => src.listBooks());
  if (books && books.length === 0) {
    problems.push("list books returned nothing");
    console.log("      no books parsed; raw catalog starts:\n" + (await rawHead("/catalog/v2/entries?count=-1")));
  }
  const book = bookArg ?? books?.[0]?.name;
  if (!book) {
    console.log("no book to test; pass one as the second argument");
    process.exit(1);
    return;
  }
  console.log(`      using book ${book}${books ? ` (${books.length} found)` : ""}`);

  const titles = await step(`suggest "${query}"`, () => src.suggest(book, query, 5));
  if (titles) {
    console.log(`      ${titles.length} title hits: ${titles.map((h) => h.path).join(", ")}`);
    if (titles.length === 0) {
      problems.push("suggest returned nothing");
      console.log("      raw suggest starts:\n" + (await rawHead(`/suggest?content=${encodeURIComponent(book)}&term=${encodeURIComponent(query)}&count=5`)));
    }
  }

  const found = await step(`full-text search "${query}"`, () => src.search(book, query, 5));
  if (found) {
    console.log(`      ${found.length} full-text hits: ${found.map((h) => h.path).join(", ")}`);
    if (found.length === 0) {
      console.log("      (empty can be normal if this ZIM has no full-text index; raw search starts:)\n" +
        (await rawHead(`/search?content=${encodeURIComponent(book)}&pattern=${encodeURIComponent(query)}&pageLength=5&format=xml`)));
    }
  }

  const target = titles?.[0] ?? found?.[0];
  if (target) {
    const article = await step(`fetch article ${target.path}`, () => src.getArticle(book, target.path));
    if (article) {
      console.log(`      title: ${article.title}; ${article.bytes} bytes; ${article.text.length} chars${article.truncated ? " (truncated)" : ""}`);
      console.log("      excerpt: " + article.text.slice(0, 200).replace(/\s+/g, " "));
      if (article.text.length < 20) problems.push("article text suspiciously short");
    }
  }

  console.log(problems.length === 0 ? "\nall steps passed" : `\n${problems.length} problem(s): ${problems.join("; ")}`);
  process.exit(problems.length === 0 ? 0 : 1);
}

main();
