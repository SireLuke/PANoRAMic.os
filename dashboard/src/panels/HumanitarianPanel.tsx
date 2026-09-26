import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const HumanitarianPanel: React.FC<Props> = ({ dashboard }) => {
    const { signals, rams } = dashboard;

    return (
        <section>
            <h2>Humanitarian</h2>
            <p>Need: {signals.humanitarianNeed}</p>
            <p>Relief: {signals.humanitarianRelief}</p>
            <p>Humanitarian RAMS OK: {rams.humanitarian.ok ? "Yes" : "No"}</p>
            <p>Reason: {rams.humanitarian.reason ?? "None"}</p>
        </section>
    );
};
