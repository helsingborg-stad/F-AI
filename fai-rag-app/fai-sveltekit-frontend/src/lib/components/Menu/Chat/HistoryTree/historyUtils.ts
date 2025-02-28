/**
 * History utilities for categorizing and organizing history items
 */
import type { HistoryItemType } from '$lib/types.js'
import {
  getDateBoundaries,
  isDateInRange,
  type DateRangeConfig,
} from '$lib/utils/dates.js'

/**
 * Extended configuration interface for testing purposes
 */
export interface ExtendedDateRangeConfig extends DateRangeConfig {
  _testDate?: Date
}

/**
 * Default category titles
 */
export const DEFAULT_CATEGORY_TITLES: Record<string, string> = {
  today: 'Today',
  yesterday: 'Yesterday',
  previous7Days: 'Previous 7 days',
  previous30Days: 'Last 30 days',
  olderItems: 'Older items',
}

/**
 * Generate category titles based on configuration
 */
export function getCategoryTitles(config: DateRangeConfig): Record<string, string> {
  const titles = { ...DEFAULT_CATEGORY_TITLES }

  // Add custom range titles if present
  if (config.customRanges) {
    config.customRanges.forEach((range) => {
      titles[range.name] = range.name
    })
  }

  return titles
}

/**
 * Function to categorize history items into time periods
 *
 * @param items History items to categorize
 * @param config Date range configuration, with optional test date
 * @returns Record with categorized items
 */
export function categorizeHistoryItems(
  items: HistoryItemType[],
  config: ExtendedDateRangeConfig,
): Record<string, HistoryItemType[]> {
  // Use _testDate for testing if provided
  const referenceDate = config._testDate
  const dateRanges = getDateBoundaries(config, referenceDate)

  // Create an empty object to store categorized items
  const categories: Record<string, HistoryItemType[]> = {}

  // Initialize all categories with empty arrays
  Object.keys(dateRanges).forEach((key) => {
    categories[key] = []
  })

  // Add a category for older items
  categories.olderItems = []

  // Sort range keys by their date values (descending - newest first)
  const sortedRangeKeys = Object.keys(dateRanges).sort(
    (a, b) => dateRanges[b].getTime() - dateRanges[a].getTime(),
  )

  // Categorize each item
  items.forEach((item) => {
    const createdDate = item.created
    let categorized = false

    // Check each range in order (from newest to oldest)
    for (let i = 0; i < sortedRangeKeys.length - 1; i++) {
      const currentKey = sortedRangeKeys[i]
      const nextKey = sortedRangeKeys[i + 1]

      if (isDateInRange(createdDate, dateRanges[nextKey], dateRanges[currentKey])) {
        categories[nextKey].push(item)
        categorized = true
        break
      }
    }

    // Check if this is in the newest range
    if (!categorized && isDateInRange(createdDate, dateRanges[sortedRangeKeys[0]])) {
      categories[sortedRangeKeys[0]].push(item)
      categorized = true
    }

    // If not categorized, it's an older item
    if (!categorized) {
      categories.olderItems.push(item)
    }
  })

  return categories
}
