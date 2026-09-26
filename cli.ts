// cli.ts

import {
    tickCommand,
    statusCommand,
    dashboardCommand,
    ramsCommand,
    signalsCommand
} from "./cli/src";

async function main() {
    const [, , cmd] = process.argv;

    switch (cmd) {
        case "tick":
            await tickCommand();
            break;
        case "status":
            statusCommand();
            break;
        case "dashboard":
            dashboardCommand();
            break;
        case "rams":
            ramsCommand();
            break;
        case "signals":
            signalsCommand();
            break;
        default:
            console.log("PANoRAMic.os CLI");
            console.log("----------------");
            console.log("Commands:");
            console.log("  tick       Run a world tick and print state");
            console.log("  status     Show world summary and key signals");
            console.log("  dashboard  Show dashboard summary in CLI");
            console.log("  rams       Run RAMS audits and print report");
            console.log("  signals    Print all global signals");
            break;
    }case "search":
    const term = process.argv[3];
    if (!term) {
        console.log("Usage: node cli search <term>");
    } else {
        searchCommand(term);
    }
    break;

}

main().catch(err => {
    console.error("CLI error:", err);
    process.exit(1);
});
