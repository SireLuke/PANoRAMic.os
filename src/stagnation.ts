export interface StagnationState {
  metric: number;
}

export function initStagnation(): StagnationState {
  return { metric: 0.2 };
}
