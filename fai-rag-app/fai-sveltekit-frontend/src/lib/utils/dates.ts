/**
 * dates.ts - Date utility functions for time-based categorization
 */

/**
 * Interface for date range configuration
 */
export interface DateRangeConfig {
  today: boolean
  yesterday: boolean
  previousDays: number[]
  customRanges?: Array<{
    name: string
    daysAgo: number
  }>
}

/**
 * Default date range configuration
 */
export const DEFAULT_DATE_RANGE_CONFIG: DateRangeConfig = {
  today: true,
  yesterday: true,
  previousDays: [7, 30],
}

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
 * Get date boundaries based on configuration
 *
 * @param config Optional configuration for date ranges
 * @param referenceDate Optional reference date (defaults to current date)
 * @returns Object with configured date boundaries
 */
export function getDateBoundaries(
  config: DateRangeConfig = DEFAULT_DATE_RANGE_CONFIG,
  referenceDate?: Date,
) {
  const now = referenceDate || new Date()
  const boundaries: Record<string, Date> = {}

  // Add standard ranges if configured
  if (config.today) {
    boundaries.today = getStartOfDay(now)
  }

  if (config.yesterday) {
    boundaries.yesterday = getDaysAgo(now, 1)
  }

  // Add previous days ranges
  if (config.previousDays && config.previousDays.length > 0) {
    config.previousDays.forEach((days) => {
      boundaries[`previous${days}Days`] = getDaysAgo(now, days)
    })
  }

  // Add any custom ranges
  if (config.customRanges && config.customRanges.length > 0) {
    config.customRanges.forEach((range) => {
      boundaries[range.name] = getDaysAgo(now, range.daysAgo)
    })
  }

  return boundaries
}
