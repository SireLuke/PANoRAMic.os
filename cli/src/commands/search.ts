// cli/src/commands/search.ts

import { initialWorld } from "../../engine/worldState";
import { aggregateSignals } from "../../engine/globalSignals";
import { runRamsTick } from "../../engine/ramsTick";
import { buildDashboard } from "../../engine/dashboard";
import { loadConfig } from "./config";

export function searchCommand(query: string) {
    const config = loadConfig();

    const world = initialWorld;
    const signals = aggregateSignals(world);
    const rams = runRamsTick(world);
    const dashboard = buildDashboard(world);

    const haystack = {
        world,
        signals,
        rams,
        dashboard
    };

    const results: Array<{ path: string; value: any }> = [];

    const q = config.search.caseSensitive ? query : query.toLowerCase();

    function scan(obj: any, prefix: string = "") {
        for (const key of Object.keys(obj)) {
            const value = obj[key];
            const path = prefix ? `${prefix}.${key}` : key;

            const keyMatch = config.search.caseSensitive
                ? key.includes(q)
                : key.toLowerCase().includes(q);

            const valueMatch =
                typeof value === "string" &&
                (config.search.caseSensitive
                    ? value.includes(q)
                    : value.toLowerCase().includes(q));

            if (keyMatch || valueMatch) {
                results.push({ path, value });
            }

            if (typeof value === "object" && value !== null) {
                scan(value, path);
            }
        }
    }

    scan(haystack);

    console.log(`Search results for "${query}":`);
    console.log("--------------------------------");

    results.slice(0, config.search.maxResults).forEach(r => {
        console.log(`${r.path}: ${JSON.stringify(r.value)}`);
    });

    if (results.length === 0) {
        console.log("No matches found.");
    }
}
