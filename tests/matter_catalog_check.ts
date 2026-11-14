import { MatterCatalog } from "../core/library/types";
import { validateMatterCatalog } from "../core/library/matterValidation";

// Declared locally so the check needs no @types/node.
declare const require: (name: string) => { readFileSync: (p: string, enc: string) => string };
declare const process: { argv: string[]; exit: (code: number) => void };

const catalog = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8")) as MatterCatalog;
const problems = validateMatterCatalog(catalog);
console.log(JSON.stringify({ nodes: catalog.nodes.length, problems }));
process.exit(problems.length === 0 ? 0 : 1);
