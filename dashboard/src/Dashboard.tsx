// dashboard/src/Dashboard.tsx

import React from "react";

import { DashboardState } from "./types";

import { WorldPanel } from "./panels/WorldPanel";
import { EconomyPanel } from "./panels/EconomyPanel";
import { GovernancePanel } from "./panels/GovernancePanel";
import { HumanitarianPanel } from "./panels/HumanitarianPanel";
import { HarmPanel } from "./panels/HarmPanel";
import { ResourcesPanel } from "./panels/ResourcesPanel";
import { PopulationPanel } from "./panels/PopulationPanel";
import { SynthesisPanel } from "./panels/SynthesisPanel";

type Props = {
    dashboard: DashboardState;
};

export const Dashboard: React.FC<Props> = ({ dashboard }) => {
    return (
        <main style={styles.container}>
            <h1 style={styles.header}>PANoRAMic.os Dashboard</h1>

            <div style={styles.grid}>
                <div style={styles.card}><WorldPanel dashboard={dashboard} /></div>
                <div style={styles.card}><EconomyPanel dashboard={dashboard} /></div>
                <div style={styles.card}><GovernancePanel dashboard={dashboard} /></div>
                <div style={styles.card}><HumanitarianPanel dashboard={dashboard} /></div>
                <div style={styles.card}><HarmPanel dashboard={dashboard} /></div>
                <div style={styles.card}><ResourcesPanel dashboard={dashboard} /></div>
                <div style={styles.card}><PopulationPanel dashboard={dashboard} /></div>
                <div style={styles.card}><SynthesisPanel dashboard={dashboard} /></div>
            </div>
        </main>
    );
};

const styles: Record<string, React.CSSProperties> = {
    container: {
        padding: "2rem",
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#111",
        color: "#eee",
        minHeight: "100vh"
    },
    header: {
        fontSize: "2.5rem",
        marginBottom: "2rem",
        textAlign: "center"
    },
    grid: {
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))",
        gap: "1.5rem"
    },
    card: {
        backgroundColor: "#1b1b1b",
        padding: "1.5rem",
        borderRadius: "12px",
        boxShadow: "0 0 12px rgba(0,0,0,0.4)"
    }
};
