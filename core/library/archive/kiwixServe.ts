/**
 * Client for kiwix-serve (https://kiwix-tools.readthedocs.io/en/latest/kiwix-serve.html), run
 * on the same machine against a ZIM file you already own, for example:
 *
 *     kiwix-serve --port 8080 wikipedia_en_all_maxi.zim
 *
 * The ZIM stays on disk and is never copied into PANoRAMic.os. Endpoints used:
 *   /catalog/v2/entries   book list (OPDS/Atom)
 *   /suggest              title suggestions (JSON)
 *   /search               full-text search (RSS/XML)
 *   /content/<book>/<p>   article HTML
 *
 * Privacy: by default only loopback addresses are accepted, nothing is cached on disk, and no
 * request carries anything but the query you typed. Remote hosts need allowRemote: true.
 *
 * The endpoint paths come from the kiwix-serve documentation. The response bodies are parsed
 * defensively, so an unexpected shape yields an empty result or an ArchiveError instead of a
 * crash; run tools/kiwix_smoke.ts against your own server to confirm it parses yours.
 */
import { ArchiveArticle, ArchiveBook, ArchiveError, ArchiveHit, ArchiveSource } from "./types";
import { decodeEntities, htmlTitle, htmlToText } from "./htmlText";
import { archiveEntryId } from "./ids";

export type FetchLike = (url: string, init?: { signal?: unknown }) => Promise<{
  ok: boolean;
  status: number;
  headers: { get(name: string): string | null };
  text(): Promise<string>;
  arrayBuffer(): Promise<ArrayBuffer>;
}>;

export interface KiwixServeOptions {
  baseUrl?: string;
  allowRemote?: boolean;
  timeoutMs?: number;
  maxArticleBytes?: number;
  maxTextChars?: number;
  /** Injected for tests; defaults to the global fetch (Node 18+, Deno, browsers). */
  fetchImpl?: FetchLike;
}

export const DEFAULT_KIWIX_URL = "http://127.0.0.1:8080";
const BOOK_NAME = /^[A-Za-z0-9._+-]{1,200}$/;
const MAX_LIMIT = 100;

export function isLoopbackHost(hostname: string): boolean {
  const h = hostname.toLowerCase().replace(/^\[|\]$/g, "");
  if (h === "localhost" || h === "::1") return true;
  const m = /^127\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.exec(h);
  return m !== null && [m[1], m[2], m[3]].every((x) => Number(x) <= 255);
}

export function validateBookName(book: string): string {
  if (typeof book !== "string" || !BOOK_NAME.test(book)) throw new ArchiveError(`invalid book name: ${JSON.stringify(book)}`);
  return book;
}

/** Validates and URL-encodes an in-archive path, segment by segment. */
export function encodeArchivePath(path: string): string {
  if (typeof path !== "string" || path === "" || path.length > 2000 || /[\u0000-\u001f]/.test(path)) {
    throw new ArchiveError("invalid archive path");
  }
  const segments = path.replace(/^\/+/, "").split("/");
  if (segments.some((s) => s === "" || s === "." || s === "..")) throw new ArchiveError("invalid archive path");
  return segments.map(encodeURIComponent).join("/");
}

function clampLimit(limit: number | undefined, fallback: number): number {
  if (limit === undefined) return fallback;
  if (!Number.isInteger(limit) || limit < 1) throw new ArchiveError("limit must be a positive integer");
  return Math.min(limit, MAX_LIMIT);
}

function stripTags(s: string): string {
  return decodeEntities(s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1").replace(/<[^>]*>/g, "")).replace(/\s+/g, " ").trim();
}

function tagText(block: string, tag: string): string | null {
  const m = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}\\s*>`, "i").exec(block);
  return m ? stripTags(m[1]) : null;
}

function blocks(xml: string, tag: string): string[] {
  const out: string[] = [];
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}\\s*>`, "gi");
  let m: RegExpExecArray | null;
  while ((m = re.exec(xml)) !== null) out.push(m[1]);
  return out;
}

function safeDecode(s: string): string {
  try { return decodeURIComponent(s); } catch { return s; }
}

export class KiwixServeSource implements ArchiveSource {
  readonly kind = "kiwix-serve";
  private readonly base: string;
  private readonly timeoutMs: number;
  private readonly maxArticleBytes: number;
  private readonly maxTextChars: number;
  private readonly fetchImpl: FetchLike;

  constructor(options: KiwixServeOptions = {}) {
    let url: URL;
    try {
      url = new URL(options.baseUrl ?? DEFAULT_KIWIX_URL);
    } catch {
      throw new ArchiveError("baseUrl is not a valid URL");
    }
    if (url.protocol !== "http:" && url.protocol !== "https:") throw new ArchiveError("baseUrl must be http or https");
    if (url.username !== "" || url.password !== "") throw new ArchiveError("baseUrl must not contain credentials");
    if (!options.allowRemote && !isLoopbackHost(url.hostname)) {
      throw new ArchiveError("refusing a non-loopback host; pass allowRemote: true to opt in");
    }
    this.base = url.origin + url.pathname.replace(/\/+$/, "");
    this.timeoutMs = options.timeoutMs ?? 10_000;
    this.maxArticleBytes = options.maxArticleBytes ?? 4_000_000;
    this.maxTextChars = options.maxTextChars ?? 200_000;
    const f = options.fetchImpl ?? ((globalThis as { fetch?: unknown }).fetch as FetchLike | undefined);
    if (!f) throw new ArchiveError("no fetch implementation available");
    this.fetchImpl = f;
  }

  private async request(path: string) {
    const Ctl = (globalThis as { AbortController?: new () => { signal: unknown; abort(): void } }).AbortController;
    const ctl = Ctl ? new Ctl() : null;
    const timer = ctl ? setTimeout(() => ctl.abort(), this.timeoutMs) : null;
    try {
      const res = await this.fetchImpl(this.base + path, ctl ? { signal: ctl.signal } : undefined);
      if (!res.ok) throw new ArchiveError(`kiwix-serve returned HTTP ${res.status}`, res.status);
      return res;
    } catch (e) {
      if (e instanceof ArchiveError) throw e;
      throw new ArchiveError(`kiwix-serve request failed: ${(e as Error).message}`);
    } finally {
      if (timer) clearTimeout(timer);
    }
  }

  async listBooks(): Promise<ArchiveBook[]> {
    const xml = await (await this.request("/catalog/v2/entries?count=-1")).text();
    const books: ArchiveBook[] = [];
    for (const entry of blocks(xml, "entry")) {
      const link = /href="[^"]*\/content\/([^"\/?#]+)[^"]*"/i.exec(entry);
      if (!link) continue;
      const name = safeDecode(link[1]);
      if (!BOOK_NAME.test(name)) continue;
      const count = tagText(entry, "articleCount");
      books.push({
        name,
        title: tagText(entry, "title") ?? name,
        language: tagText(entry, "language"),
        articleCount: count !== null && /^\d+$/.test(count) ? Number(count) : null,
      });
    }
    return books;
  }

  async suggest(book: string, term: string, limit?: number): Promise<ArchiveHit[]> {
    validateBookName(book);
    if (typeof term !== "string" || term.trim() === "") return [];
    const n = clampLimit(limit, 10);
    const body = await (await this.request(
      `/suggest?content=${encodeURIComponent(book)}&term=${encodeURIComponent(term)}&count=${n}`,
    )).text();
    let data: unknown;
    try { data = JSON.parse(body); } catch { throw new ArchiveError("kiwix-serve /suggest did not return JSON"); }
    if (!Array.isArray(data)) return [];
    const hits: ArchiveHit[] = [];
    for (const raw of data) {
      const item = raw as { value?: unknown; label?: unknown; path?: unknown };
      if (typeof item.path !== "string" || item.path === "") continue; // full-text pseudo-suggestion
      const title = stripTags(String(item.value ?? item.label ?? item.path));
      hits.push({ id: archiveEntryId(book, item.path), book, path: item.path, title, snippet: "" });
    }
    return hits.slice(0, n);
  }

  async search(book: string, query: string, limit?: number): Promise<ArchiveHit[]> {
    validateBookName(book);
    if (typeof query !== "string" || query.trim() === "") return [];
    const n = clampLimit(limit, 10);
    const xml = await (await this.request(
      `/search?content=${encodeURIComponent(book)}&pattern=${encodeURIComponent(query)}&pageLength=${n}&format=xml`,
    )).text();
    const hits: ArchiveHit[] = [];
    for (const item of blocks(xml, "item")) {
      const link = tagText(item, "link");
      if (!link) continue;
      const marker = `/content/${book}/`;
      const at = link.indexOf(marker);
      if (at < 0) continue;
      const path = safeDecode(link.slice(at + marker.length).split(/[?#]/)[0]);
      if (path === "") continue;
      hits.push({
        id: archiveEntryId(book, path), book, path,
        title: tagText(item, "title") ?? path,
        snippet: tagText(item, "description") ?? "",
      });
    }
    return hits.slice(0, n);
  }

  async getArticle(book: string, path: string): Promise<ArchiveArticle> {
    validateBookName(book);
    const encoded = encodeArchivePath(path);
    const res = await this.request(`/content/${encodeURIComponent(book)}/${encoded}`);
    const type = (res.headers.get("content-type") ?? "").toLowerCase();
    if (type !== "" && !type.includes("html") && !type.startsWith("text/")) {
      throw new ArchiveError(`entry is ${type}, not a text document`);
    }
    const buf = await res.arrayBuffer();
    if (buf.byteLength > this.maxArticleBytes) {
      throw new ArchiveError(`entry is ${buf.byteLength} bytes, over the ${this.maxArticleBytes} byte limit`);
    }
    const html = new TextDecoder("utf-8").decode(buf);
    const full = htmlToText(html);
    const truncated = full.length > this.maxTextChars;
    const cleanPath = path.replace(/^\/+/, "");
    return {
      id: archiveEntryId(book, cleanPath),
      book,
      path: cleanPath,
      title: htmlTitle(html),
      text: truncated ? full.slice(0, this.maxTextChars) : full,
      truncated,
      bytes: buf.byteLength,
    };
  }
}
