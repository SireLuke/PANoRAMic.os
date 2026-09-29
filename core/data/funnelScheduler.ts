// core/data/funnelScheduler.ts

import { processFunnelData } from "./funnelManager"

/**
 * Funnel Scheduler:
 * Runs funnel ingestion at timed intervals.
 */

export type FunnelSchedule = {
  type: string
  intervalMs: number
  fetcher: () => Promise<any>
}

export class FunnelScheduler {
  private schedules: FunnelSchedule[] = []
  private world: any
  private pillarDefaults: any

  constructor(world: any, pillarDefaults: any) {
    this.world = world
    this.pillarDefaults = pillarDefaults
  }

  addSchedule(schedule: FunnelSchedule) {
    this.schedules.push(schedule)
  }

  start() {
    this.schedules.forEach(schedule => {
      setInterval(async () => {
        try {
          const incoming = await schedule.fetcher()
          this.world = processFunnelData(
            this.world,
            incoming,
            this.pillarDefaults
          )
        } catch (err) {
          console.error(`Funnel schedule error (${schedule.type}):`, err)
        }
      }, schedule.intervalMs)
    })
  }

  getWorld() {
    return this.world
  }
}