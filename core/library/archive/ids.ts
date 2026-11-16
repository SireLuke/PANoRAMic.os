/** Stable ids for archive entries: "kiwix:<book>:<path>". Book names never contain ":". */

export function archiveEntryId(book: string, path: string): string {
  return `kiwix:${book}:${path.replace(/^\/+/, "")}`;
}

export function parseArchiveEntryId(id: string): { book: string; path: string } | null {
  const m = /^kiwix:([A-Za-z0-9._+-]+):(.+)$/.exec(id);
  return m ? { book: m[1], path: m[2] } : null;
}
