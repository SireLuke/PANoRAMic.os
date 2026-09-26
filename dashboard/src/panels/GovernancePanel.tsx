import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const GovernancePanel: React.FC<Props> = ({ dashboard }) => {
    const { signals, rams } = dashboard;

    return (
        <section>
            <h2>Governance</h2>
            <p>Panitarian Score: {signals.governance}</p>
            <p>Governance RAMS OK: {rams.governance.ok ? "Yes" : "No"}</p>
            <p>Governance Reason: {rams.governance.reason ?? "None"}</p>
        </section>
    );
};
