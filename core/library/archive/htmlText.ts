/**
 * Small, dependency-free HTML to plain-text conversion for archive articles.
 * The output is text for reading and indexing; it is not sanitized HTML and must not be
 * inserted into a page as markup.
 */

const NAMED: { [name: string]: string } = {
  amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "–", mdash: "—",
  hellip: "…", lsquo: "‘", rsquo: "’", ldquo: "“", rdquo: "”",
  minus: "−", times: "×", deg: "°", plusmn: "±",
};

function fromCodePoint(n: number): string {
  if (!Number.isFinite(n) || n <= 0 || n > 0x10ffff || (n >= 0xd800 && n <= 0xdfff)) return "�";
  return String.fromCodePoint(n);
}

export function decodeEntities(s: string): string {
  return s.replace(/&(#x[0-9a-fA-F]{1,6}|#[0-9]{1,7}|[A-Za-z][A-Za-z0-9]{1,8});/g, (whole, body: string) => {
    if (body[0] === "#") {
      const hex = body[1] === "x" || body[1] === "X";
      return fromCodePoint(parseInt(body.slice(hex ? 2 : 1), hex ? 16 : 10));
    }
    const hit = NAMED[body];
    return hit === undefined ? whole : hit;
  });
}

export function htmlToText(html: string): string {
  let s = html;
  s = s.replace(/<!--[\s\S]*?-->/g, " ");
  s = s.replace(/<(script|style|noscript|head|svg)\b[\s\S]*?<\/\1\s*>/gi, " ");
  s = s.replace(/<\s*br\s*\/?\s*>/gi, "\n");
  s = s.replace(/<\/\s*(p|div|h[1-6]|li|tr|ul|ol|table|section|blockquote|pre)\s*>/gi, "\n");
  s = s.replace(/<[^>]*>/g, "");
  s = decodeEntities(s);
  s = s.replace(/[ \t\f\v ]+/g, " ");
  s = s.replace(/ *\n */g, "\n");
  s = s.replace(/\n{3,}/g, "\n\n");
  return s.trim();
}

/** Text of the first <title> element, or null. */
export function htmlTitle(html: string): string | null {
  const m = /<title\b[^>]*>([\s\S]*?)<\/title\s*>/i.exec(html);
  if (!m) return null;
  const t = decodeEntities(m[1].replace(/<[^>]*>/g, "")).replace(/\s+/g, " ").trim();
  return t === "" ? null : t;
}
