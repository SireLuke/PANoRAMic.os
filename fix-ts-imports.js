import fs from "fs";
import path from "path";

const root = process.cwd();

function walk(dir) {
  for (const file of fs.readdirSync(dir)) {
    const full = path.join(dir, file);
    const stat = fs.statSync(full);

    if (stat.isDirectory()) {
      walk(full);
    } else if (file.endsWith(".ts") || file.endsWith(".tsx")) {
      fixFile(full);
    }
  }
}

function fixFile(filePath) {
  let content = fs.readFileSync(filePath, "utf8");

  // Replace .js imports with .ts imports
  const fixed = content.replace(
    /from\s+["'](\.\/[^"']+|\.{2}\/[^"']+)\.js["']/g,
    (match, p1) => {
      return `from "${p1}.ts"`;
    }
  );

  if (fixed !== content) {
    fs.writeFileSync(filePath, fixed, "utf8");
    console.log("Fixed:", filePath);
  }
}

walk(root);
console.log(".ts import fix complete.");
