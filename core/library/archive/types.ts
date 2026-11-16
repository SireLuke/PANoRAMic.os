/**
 * Archive layer for the Library of Alexandria.
 *
 * An ArchiveSource is a read-only, offline body of reference text (for example a Kiwix ZIM
 * served on the same machine). Archive entries are NOT LibraryNodes: a LibraryNode carries
 * culture and nuance fields that nobody has assessed for an encyclopedia article, so this
 * layer never invents them. An entry is only promoted to a LibraryNode when the caller
 * supplies those fields (see bridge.ts).
 *
 * Nothing here is a scientific or physical claim. The archive is a source of text, and the
 * text is only as reliable as whoever wrote it.
 */

export interface ArchiveBook {
  /** Identifier used in URLs (for kiwix-serve, the ZIM name derived from the file name). */
  name: string;
  title: string;
  language: string | null;
  articleCount: number | null;
}

/** A pointer to an article, with no body. */
export interface ArchiveHit {
  /** "kiwix:<book>:<path>", see archiveEntryId. */
  id: string;
  book: string;
  /** Path inside the archive, decoded (for example "A/Fermi_gas"). */
  path: string;
  title: string;
  snippet: string;
}

export interface ArchiveArticle {
  id: string;
  book: string;
  path: string;
  title: string | null;
  /** Plain text only. Never render it as HTML. */
  text: string;
  /** True when text was cut at the configured limit. */
  truncated: boolean;
  /** Size of the raw document as received, in bytes. */
  bytes: number;
}

export interface ArchiveSource {
  readonly kind: string;
  listBooks(): Promise<ArchiveBook[]>;
  /** Title-prefix suggestions. Fast. */
  suggest(book: string, term: string, limit?: number): Promise<ArchiveHit[]>;
  /** Full-text search. Slower, and needs the ZIM to carry a full-text index. */
  search(book: string, query: string, limit?: number): Promise<ArchiveHit[]>;
  getArticle(book: string, path: string): Promise<ArchiveArticle>;
}

export class ArchiveError extends Error {
  constructor(message: string, readonly status: number | null = null) {
    super(message);
    this.name = "ArchiveError";
  }
}
