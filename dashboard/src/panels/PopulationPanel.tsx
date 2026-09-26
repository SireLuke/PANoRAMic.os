import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const PopulationPanel: React.FC<Props> = ({ dashboard }) => {
    const { signals, world } = dashboard;

    return (
        <section>
            <h2>Population</h2>
            <p>Total: {signals.population}</p>
            <p>Births (last tick): {world.population.births ?? 0}</p>
            <p>Deaths (last tick): {world.population.deaths ?? 0}</p>
            <p>Migration Change (last tick): {world.population.migrationChange ?? 0}</p>
        </section>
    );
};
