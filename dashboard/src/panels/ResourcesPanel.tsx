import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const ResourcesPanel: React.FC<Props> = ({ dashboard }) => {
    const { signals, rams } = dashboard;

    return (
        <section>
            <h2>Resources</h2>
            <p>Resource Score: {signals.resources}</p>
            <p>Scarcity: {signals.scarcity}</p>
            <p>Sustainability: {signals.sustainability}</p>
            <p>Resources RAMS OK: {rams.resources.ok ? "Yes" : "No"}</p>
            <p>Reason: {rams.resources.reason ?? "None"}</p>
        </section>
    );
};
