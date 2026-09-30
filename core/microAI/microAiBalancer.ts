// core/microAI/microAiBalancer.ts

/**
 * Micro-AI Load Balancer:
 * Prevents PAN-OS from overloading itself by regulating ingestion frequency,
 * CPU load, memory usage, and funnel throughput.
 */

export class MicroAiBalancer {
  private lastIngestionTime = 0
  private minIntervalMs = 200   // throttle ingestion to 5 updates/sec
  private maxCpuLoad = 0.85     // do not process if CPU load too high
  private maxMemoryUse = 0.85   // do not process if memory too high

  private cpuLoadFn: () => number
  private memoryFn: () => number

  constructor(cpuLoadFn: () => number, memoryFn: () => number) {
    this.cpuLoadFn = cpuLoadFn
    this.memoryFn = memoryFn
  }

  canProcess(): boolean {
    const now = Date.now()

    // Throttle ingestion frequency
    if (now - this.lastIngestionTime < this.minIntervalMs) {
      return false
    }

    // CPU load check
    const cpuLoad = this.cpuLoadFn()
    if (cpuLoad > this.maxCpuLoad) {
      console.warn("Micro-AI: CPU load too high, delaying ingestion.")
      return false
    }

    // Memory check
    const memLoad = this.memoryFn()
    if (memLoad > this.maxMemoryUse) {
      console.warn("Micro-AI: Memory usage too high, delaying ingestion.")
      return false
    }

    this.lastIngestionTime = now
    return true
  }
}