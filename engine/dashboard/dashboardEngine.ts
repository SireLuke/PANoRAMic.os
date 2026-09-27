// engine/dashboard/dashboardEngine.ts

let dashboardState: any = {}

export const dashboardEngine = {
  update(update: any) {
    dashboardState = {
      tick: update.tick ?? dashboardState.tick ?? 0,

      // NodeMap
      nodeMap: update.nodeMap ?? dashboardState.nodeMap,
      nodeSignals: update.nodeSignals ?? dashboardState.nodeSignals,
      nodeAudits: update.nodeAudits ?? dashboardState.nodeAudits,

      // Pillars
      par: update.parState ?? dashboardState.par,
      rights: update.rightsState ?? dashboardState.rights,
      ecology: update.ecologyState ?? dashboardState.ecology,
      infrastructure: update.infraState ?? dashboardState.infrastructure,
      commons: update.commonsState ?? dashboardState.commons,
      governance: update.governanceState ?? dashboardState.governance,
      labor: update.laborState ?? dashboardState.labor,
      markets: update.marketsState ?? dashboardState.markets,
      population: update.populationState ?? dashboardState.population,
      workforce: update.workforceState ?? dashboardState.workforce,

      // Modes
      modesState: update.modesState ?? dashboardState.modesState,

      // RAMS
      systemAudits: update.systemAudits ?? dashboardState.systemAudits,
      audits: update.audits ?? dashboardState.audits,

      // Signals
      signals: update.signals ?? dashboardState.signals,

      // Global/System
      globalState: update.globalState ?? dashboardState.globalState,
      systemState: update.systemState ?? dashboardState.systemState,
    }
  },

  getState() {
    return dashboardState
  }
}
