import { bootSystem } from "../src/boot.ts";

async function main() {
  await bootSystem();
}

main().catch((err) => {
  console.error("PAN startup error:", err);
  process.exit(1);
});
