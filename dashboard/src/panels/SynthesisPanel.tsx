import React from "react";
import { DashboardState } from "../types";

type Props = {
    dashboard: DashboardState;
};

export const SynthesisPanel: React.FC<Props> = ({ dashboard }) => {
    const { world } = dashboard;

    return (
        <section>
            <h2>Synthesis</h2>
            <p>Coherence Score: {world.synthesis.coherenceScore ?? 0}</p>
            <pre>{JSON.stringify(world.synthesis.vector, null, 2)}</pre>
        </section>
    );
};
