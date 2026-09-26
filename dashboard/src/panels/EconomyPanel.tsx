import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const EconomyPanel: React.FC<Props> = ({ dashboard }) => {
    const { world, signals } = dashboard;

    return (
        <section>
            <h2>Economy</h2>
            <p>PAR Supply: {signals.parSupply}</p>
            <p>PAR Cap: {signals.parCap}</p>
            <p>Stewardship Fund: {signals.stewardship}</p>
            <p>Humanitarian Pool: {signals.humanitarianPool}</p>
            <p>Tax Load: {signals.taxLoad}</p>
        </section>
    );
};
