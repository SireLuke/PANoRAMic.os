import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const HarmPanel: React.FC<Props> = ({ dashboard }) => {
    const { signals, rams } = dashboard;

    return (
        <section>
            <h2>Harm Index</h2>
            <p>Harm Score: {signals.harm}</p>
            <p>Harm RAMS OK: {rams.harm.ok ? "Yes" : "No"}</p>
            <p>Reason: {rams.harm.reason ?? "None"}</p>
        </section>
    );
};
