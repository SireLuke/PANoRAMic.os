/**
 * Runtime checks for a MatterCatalog (see types.ts). Returns a list of problems; empty means consistent.
 * These are structural checks only: they do not verify any value against a primary source.
 */
import { MatterCatalog, MatterNode, V8Coordinate } from "./types";

const COORDS: V8Coordinate[] = ["h", "R", "u", "d", "tau", "chi", "s", "f"];

function checkV8(node: MatterNode, problems: string[]): void {
  for (const k of COORDS) {
    if (!(k in node.v8)) {
      problems.push(`${node.id}: v8 missing ${k}`);
      continue;
    }
    const v = node.v8[k];
    if (v === null) continue;
    const lo = k === "chi" ? -1 : 0;
    if (typeof v !== "number" || !isFinite(v) || v < lo || v > 1) {
      problems.push(`${node.id}: v8.${k}=${v} outside [${lo}, 1]`);
    }
  }
}

export function validateMatterCatalog(catalog: MatterCatalog): string[] {
  const problems: string[] = [];
  const sourceIds = new Set(catalog.sources.map((s) => s.id));
  const seen = new Set<string>();
  const cells = new Set<string>();
  for (const n of catalog.nodes) {
    if (seen.has(n.id)) problems.push(`${n.id}: duplicate id`);
    seen.add(n.id);
    if (!n.id.startsWith(`matter:${n.kind}:`)) problems.push(`${n.id}: id does not match kind ${n.kind}`);
    checkV8(n, problems);
    if (n.v8.tau !== null || n.v8.f !== null) problems.push(`${n.id}: tau/f are unassigned in v0`);
    for (const id of n.sourceIds) if (!sourceIds.has(id)) problems.push(`${n.id}: unknown source ${id}`);
    for (const m of n.measured) if (!sourceIds.has(m.sourceId)) problems.push(`${n.id}: unknown source ${m.sourceId}`);
    if (n.kind === "element") {
      if (!n.element || n.molecule) problems.push(`${n.id}: element node needs element data only`);
      else {
        const g = n.element.grid;
        if (g.row < 1 || g.row > 9 || g.col < 1 || g.col > 18) problems.push(`${n.id}: grid out of range`);
        const key = `${g.row},${g.col}`;
        if (cells.has(key)) problems.push(`${n.id}: grid cell ${key} reused`);
        cells.add(key);
        if (g.block === "f" && g.group !== null) problems.push(`${n.id}: f-block with a group`);
      }
      if (!n.v8Mapping) problems.push(`${n.id}: element without a V8 mapping reference`);
      else if (n.v8Mapping.claimLevel !== "declared-hypothesis" || n.v8Mapping.schemaOwner !== "pan-fractal-kernel") {
        problems.push(`${n.id}: unexpected mapping claim level or owner`);
      }
    } else {
      if (!n.molecule || n.element) problems.push(`${n.id}: molecule/ion node needs molecule data only`);
      if (n.v8Mapping !== null) problems.push(`${n.id}: no V8 map is declared for ${n.kind}`);
      if (COORDS.some((k) => n.v8[k] !== null)) problems.push(`${n.id}: molecule V8 state must be all null`);
      if ((n.kind === "ion") !== (n.molecule !== null && n.molecule.charge !== 0)) {
        problems.push(`${n.id}: kind and charge disagree`);
      }
    }
    for (const v of n.views) {
      if ((v.status === "available") !== (v.ref !== null)) problems.push(`${n.id}: view ${v.kind} status/ref mismatch`);
    }
  }
  return problems;
}
