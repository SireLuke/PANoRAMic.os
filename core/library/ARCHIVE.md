# Library of Alexandria: offline archive source (Kiwix)

The Library can read a local Kiwix archive (a `.zim` file such as an offline Wikipedia) through
`kiwix-serve`. The archive stays on disk where it is. Nothing is copied into PANoRAMic.os, no
article is stored unless you promote it, and no request leaves your machine by default.

## Set up on your own computer

1. Get `kiwix-serve` (part of [kiwix-tools](https://kiwix-tools.readthedocs.io/en/latest/kiwix-serve.html);
   Kiwix desktop also bundles it).
2. Serve your file. A large ZIM is memory-mapped, so start-up is quick and RAM use is modest:

   ```
   kiwix-serve --port 8080 /path/to/wikipedia_en_all_maxi.zim
   ```

3. Check that the adapter understands your Kiwix version. From the repository root:

   ```
   mkdir -p /tmp/pan-smoke && cd /tmp/pan-smoke
   npx -p typescript tsc --target ES2020 --module commonjs --skipLibCheck --outDir out <repo>/tools/kiwix_smoke.ts
   node out/tools/kiwix_smoke.js http://127.0.0.1:8080
   ```

   (`out/tools/` is where `tsc` puts it when it also compiles `core/library/archive`. If the path
   differs, `find out -name kiwix_smoke.js`.) It lists your books, runs a title suggestion, a
   full-text search and an article fetch, and prints a short excerpt. If a step comes back empty it
   prints the start of the raw response; send that if something does not parse.

## Use

```ts
import { KiwixServeSource, findInArchive, promoteToNode } from "./core/library/archive";
import { libraryOfAlexandria } from "./core/library/libraryOfAlexandria";

const kiwix = new KiwixServeSource({ baseUrl: "http://127.0.0.1:8080" });
const [book] = await kiwix.listBooks();

const hits = await findInArchive(kiwix, book.name, "Fermi gas", 10); // titles + full text, merged
const article = await kiwix.getArticle(book.name, hits[0].path);      // plain text, never HTML

// Optional: keep an article as a LibraryNode. Culture and nuance are YOUR input, never inferred.
promoteToNode(libraryOfAlexandria, article, myCulture, myNuance);
```

`archiveRoutes(source)` returns framework-neutral handlers (`books`, `suggest`, `search`,
`article`) that give `{ status, body }`, so any server can mount them.

## Design rules

- **Archive entries are not LibraryNodes.** A LibraryNode has culture and nuance fields. Nobody has
  assessed those for an encyclopedia article, so the archive layer does not make them up; it only
  creates a node when you hand it those fields. Entry ids look like `kiwix:<book>:<path>`.
- **No surveillance.** Only loopback hosts are accepted unless you pass `allowRemote: true`. No
  disk writes, no cache, no telemetry, no credentials in the URL. The only thing sent is the
  query you typed.
- **Bounded.** Request timeout 10 s, article limit 4 MB, text limit 200k characters, result limit
  100, book names and in-archive paths validated before any request.
- **Text only.** `htmlToText` removes scripts, styles and tags. The result is for reading and
  indexing, not for inserting into a page as markup.
- **Default trust is a placeholder.** `ARCHIVE_DEFAULT_TRUST = 0.5` is neutral, not an assessment.
  Promoted nodes record `community` provenance and an empty verification chain.
- **Not baked in.** The archive is an optional source behind the `ArchiveSource` interface. Another
  backend (for example `libzim` bindings reading the file directly) can implement the same four
  methods without touching anything else.

## Evidence status

This is a software adapter with no scientific claim, so no Lean statement applies.

| Check | Status |
| --- | --- |
| Adapter behaviour against a fake `kiwix-serve` built from the documented endpoints (`tests/library_archive_check.ts`) | tested; mutation-checked for the loopback, path and script-stripping guards |
| Endpoint paths and query parameters | taken from the kiwix-serve documentation |
| Response formats of your installed `kiwix-serve` (`/suggest` JSON, `/search` XML, OPDS catalog) | `not_tested` until `tools/kiwix_smoke.ts` has run against a real server |
| Behaviour on a full-size Wikipedia ZIM (latency, memory) | `not_tested` |

## Not built yet

- The zoom ladder and the compound-eye mosaic layer over the archive.
- Any mapping of articles to V8 coordinates (the element map in `types.ts` is separate, and the V8
  schema belongs to pan-fractal-kernel).
- Bulk indexing or embedding of the archive.
- Full-text search needs a ZIM built with a full-text index; without one only title suggestions work,
  and `findInArchive` falls back to titles.
