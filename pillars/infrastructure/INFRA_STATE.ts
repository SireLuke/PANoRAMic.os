export interface InfrastructureState {
  resilienceIndex: number
  failureIndex: number
}

export const defaultInfrastructureState: InfrastructureState = {
  resilienceIndex: 0.8,
  failureIndex: 0.1,
}
