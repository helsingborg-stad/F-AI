import { m } from '$lib/paraglide/messages.js'
import type { HistoryItemType } from '$lib/types.js'
import {
  getDateBoundaries,
  isDateInRange,
  type IDateRangeConfig,
} from '$lib/utils/dates.js'
import dayjs from 'dayjs'

export const DEFAULT_CATEGORY_TITLES: Record<string, string> = {
  today: m.chat_history_category_today(),
  yesterday: m.chat_history_category_yesterday(),
  previous7Days: m.chat_history_category_previous_7_days(),
  previous30Days: m.chat_history_category_previous_30_days(),
  olderItems: m.chat_history_category_older_items(),
}

export function getCategoryTitles(config: IDateRangeConfig): Record<string, string> {
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
 * @param referenceDate Optional reference date for testing or overriding current date
 * @returns Record with categorized items
 */
export function categorizeHistoryItems(
  items: HistoryItemType[],
  config: IDateRangeConfig,
  referenceDate?: Date,
): Record<string, HistoryItemType[]> {
  const dateRanges = getDateBoundaries(config, referenceDate)

  const categories: Record<string, HistoryItemType[]> = {}

  Object.keys(dateRanges).forEach((key) => {
    categories[key] = []
  })

  categories.olderItems = []

  const sortedRangeKeys = Object.keys(dateRanges).sort(
    (a, b) => dateRanges[b].getTime() - dateRanges[a].getTime(),
  )

  items.forEach((item) => {
    const createdDate = dayjs(item.createdTimestamp).toDate()
    let categorized = false

    for (let i = 0; i < sortedRangeKeys.length - 1; i++) {
      const currentKey = sortedRangeKeys[i]
      const nextKey = sortedRangeKeys[i + 1]

      if (isDateInRange(createdDate, dateRanges[nextKey], dateRanges[currentKey])) {
        categories[nextKey].push(item)
        categorized = true
        break
      }
    }

    if (!categorized && isDateInRange(createdDate, dateRanges[sortedRangeKeys[0]])) {
      categories[sortedRangeKeys[0]].push(item)
      categorized = true
    }

    if (!categorized) {
      categories.olderItems.push(item)
    }
  })

  return categories
}
