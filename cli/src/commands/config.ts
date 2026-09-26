// cli/src/commands/config.ts

import fs from "fs";
import path from "path";

export function loadConfig() {
    const file = path.resolve("cli.config.json");

    try {
        const raw = fs.readFileSync(file, "utf8");
        return JSON.parse(raw);
    } catch {
        console.warn("Could not load cli.config.json, using defaults.");
        return {
            tickSpeed: 1000,
            outputStyle: "pretty",
            theme: "dark",
            ramsVerbosity: "normal",
            search: {
                caseSensitive: false,
                maxResults: 25
            }
        };
    }
}
