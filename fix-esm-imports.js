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

  // Regex: find imports missing .js extension
  const fixed = content.replace(
    /from\s+["'](\.\/[^"']+|\.{2}\/[^"']+)["']/g,
    (match, p1) => {
      // If already has extension, leave it alone
      if (p1.endsWith(".js") || p1.endsWith(".json")) return match;
      return `from "${p1}.js"`;
    }
  );

  if (fixed !== content) {
    fs.writeFileSync(filePath, fixed, "utf8");
    console.log("Fixed:", filePath);
  }
}

walk(root);
console.log("ESM import fix complete.");
