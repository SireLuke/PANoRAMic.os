import { ModesState } from "../../pillars/modes/MODES_STATE"

export function emitModesSignals(state: ModesState) {
  return {
    active: state.activeMode,
    stability: state.stabilityIndex,
    responsiveness: state.responsivenessIndex,
    autonomy: state.autonomyLevel,
    safety: state.safetyLevel,
    transitionRate: state.modeTransitionRate,
  }
}
