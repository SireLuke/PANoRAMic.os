import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const WorldPanel: React.FC<Props> = ({ dashboard }) => {
    const { world, signals } = dashboard;

    return (
        <section>
            <h2>World Overview</h2>
            <p>Population: {world.population.total ?? 0}</p>
            <p>Risk: {signals.risk}</p>
            <p>Resilience: {signals.resilience}</p>
            <p>Volatility: {signals.volatility}</p>
        </section>
    );
};
