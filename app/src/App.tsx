import React, { useState, useEffect } from "react";

import { initWorld } from "@engine/world/initWorld";
import { tick } from "@engine/world/tick";
import { buildDashboard } from "@engine/world/dashboard";

export default function App() {
  const [world, setWorld] = useState(() => initWorld([]));
  const [dashboard, setDashboard] = useState(() => {
    const initial = initWorld([]);
    return buildDashboard({
      world: initial,
      signals: initial.synthesis,
      tick: initial.tick,
    });
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const result = tick(world);
      setWorld(result.world);
      setDashboard(
        buildDashboard({
          world: result.world,
          signals: result.signals,
          tick: result.tick,
        })
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [world]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>PANoRAMic.os</h1>
      <pre>{JSON.stringify(dashboard, null, 2)}</pre>
    </div>
  );
}
