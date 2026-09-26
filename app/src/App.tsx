import React, { useState, useEffect } from "react";

import { Dashboard } from "@dashboard/Dashboard";
import { buildDashboard } from "@engine/dashboard";
import { reduceWorld } from "@engine/worldReducer";
import { initialWorld } from "@engine/worldState";

export default function App() {
  const [world, setWorld] = useState(initialWorld);
  const [dashboard, setDashboard] = useState(buildDashboard(initialWorld));

  useEffect(() => {
    const interval = setInterval(() => {
      const next = reduceWorld(world);
      setWorld(next);
      setDashboard(buildDashboard(next));
    }, 1000); // 1 tick per second

    return () => clearInterval(interval);
  }, [world]);

  return (
    <div style={{ padding: "2rem" }}>
      <Dashboard dashboard={dashboard} />
    </div>
  );
}
