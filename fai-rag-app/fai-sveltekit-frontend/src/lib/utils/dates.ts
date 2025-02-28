/**
 * Date utility functions
 */

/**
 * Get date with time set to midnight (start of day)
 */
export function getStartOfDay(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate())
}

/**
 * Get a date X days ago from the provided date, set to midnight
 */
export function getDaysAgo(date: Date, days: number): Date {
  const result = getStartOfDay(new Date(date))
  result.setDate(result.getDate() - days)
  return result
}

/**
 * Check if a date falls within a date range
 */
export function isDateInRange(date: Date, startDate: Date, endDate?: Date): boolean {
  const timestamp = date.getTime()
  return timestamp >= startDate.getTime() && (!endDate || timestamp < endDate.getTime())
}

/**
 * Get standard date boundaries from current date
 * Returns an object with today, yesterday, 7 days ago and 30 days ago
 */
export function getDateBoundaries(referenceDate?: Date) {
  const now = referenceDate || new Date()
  return {
    today: getStartOfDay(now),
    yesterday: getDaysAgo(now, 1),
    previousSevenDays: getDaysAgo(now, 7),
    previousThirtyDays: getDaysAgo(now, 30),
  }
}
