/**
 * Framework-neutral handlers for the archive. Each takes the parsed query parameters and returns
 * { status, body }, so any server (Express, Deno, the future api/server.ts) can mount them.
 * Article text is returned as plain text; clients must not render it as HTML.
 */
import { ArchiveError, ArchiveSource } from "./types";
import { encodeArchivePath, validateBookName } from "./kiwixServe";
import { findInArchive } from "./bridge";

export type Query = { [key: string]: string | undefined };
export interface RouteResult { status: number; body: unknown }

const bad = (message: string): RouteResult => ({ status: 400, body: { error: message } });

async function guarded(run: () => Promise<unknown>): Promise<RouteResult> {
  try {
    return { status: 200, body: await run() };
  } catch (e) {
    if (e instanceof ArchiveError) return { status: 502, body: { error: e.message } };
    return { status: 500, body: { error: "internal error" } };
  }
}

function limitOf(q: Query): number | RouteResult {
  if (q.limit === undefined) return 10;
  if (!/^\d{1,3}$/.test(q.limit) || Number(q.limit) < 1) return bad("limit must be a positive integer");
  return Number(q.limit);
}

export function archiveRoutes(source: ArchiveSource) {
  return {
    books: (): Promise<RouteResult> => guarded(() => source.listBooks()),

    suggest(q: Query): Promise<RouteResult> {
      const limit = limitOf(q);
      if (typeof limit !== "number") return Promise.resolve(limit);
      try { validateBookName(q.book ?? ""); } catch (e) { return Promise.resolve(bad((e as Error).message)); }
      if (!q.term) return Promise.resolve(bad("term is required"));
      return guarded(() => source.suggest(q.book as string, q.term as string, limit));
    },

    search(q: Query): Promise<RouteResult> {
      const limit = limitOf(q);
      if (typeof limit !== "number") return Promise.resolve(limit);
      try { validateBookName(q.book ?? ""); } catch (e) { return Promise.resolve(bad((e as Error).message)); }
      if (!q.q) return Promise.resolve(bad("q is required"));
      return guarded(() => findInArchive(source, q.book as string, q.q as string, limit));
    },

    article(q: Query): Promise<RouteResult> {
      try {
        validateBookName(q.book ?? "");
        encodeArchivePath(q.path ?? "");
      } catch (e) {
        return Promise.resolve(bad((e as Error).message));
      }
      return guarded(() => source.getArticle(q.book as string, q.path as string));
    },
  };
}
