export interface InfrastructureMetrics {
  stability: number
  load: number
  efficiency: number
}

export function computeInfrastructureMetrics(): InfrastructureMetrics {
  return {
    stability: 0.8,
    load: 0.3,
    efficiency: 0.9,
  }
}
