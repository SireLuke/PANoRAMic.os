// core/data/worldExports.ts

import {
  getWorldSnapshot as _getWorldSnapshot,
  getWorldDiff as _getWorldDiff,
  getGlobalAlerts as _getGlobalAlerts,
  getForecastHistory as _getForecastHistory,
  getEventLog as _getEventLog
} from "./funnels/libraryOfAlexandria"

export function getWorldSnapshot() {
  return _getWorldSnapshot()
}

export function getWorldDiff() {
  return _getWorldDiff()
}

export function getGlobalAlerts() {
  return _getGlobalAlerts()
}

export function getForecastHistory() {
  return _getForecastHistory()
}

export function getEventLog() {
  return _getEventLog()
}