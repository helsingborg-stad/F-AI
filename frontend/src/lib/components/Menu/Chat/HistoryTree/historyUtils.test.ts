import { describe, it, expect, beforeEach } from 'vitest'
import {
  getCategoryTitles,
  categorizeHistoryItems,
} from '$lib/components/Menu/Chat/HistoryTree/historyUtils.js'
import type { HistoryItemType } from '$lib/types.js'
import type { IDateRangeConfig } from '$lib/utils/dates.js'

describe('getCategoryTitles', () => {
  it('should return default category titles', () => {
    const config: IDateRangeConfig = {
      today: true,
      yesterday: true,
      previousDays: [7, 30],
    }

    const titles = getCategoryTitles(config)

    expect(titles.today).toBe('Today')
    expect(titles.yesterday).toBe('Yesterday')
    expect(titles.previous7Days).toBe('Previous 7 days')
    expect(titles.previous30Days).toBe('Last 30 days')
    expect(titles.olderItems).toBe('Older items')
  })

  it('should include custom category titles', () => {
    const config: IDateRangeConfig = {
      today: true,
      yesterday: true,
      previousDays: [7],
      customRanges: [
        { name: 'lastQuarter', daysAgo: 90 },
        { name: 'lastYear', daysAgo: 365 },
      ],
    }

    const titles = getCategoryTitles(config)

    expect(titles.today).toBe('Today')
    expect(titles.lastQuarter).toBe('lastQuarter')
    expect(titles.lastYear).toBe('lastYear')
  })
})

describe('categorizeHistoryItems', () => {
  // For testing purposes, we'll create a custom implementation of getDateBoundaries
  // that returns predictable dates for our test data
  const testDate = new Date('2023-05-15T00:00:00.000Z') // May 15, 2023 at midnight UTC

  let items: HistoryItemType[]

  const standardConfig: IDateRangeConfig = {
    today: true,
    yesterday: true,
    previousDays: [7, 30],
  }

  beforeEach(() => {
    items = [
      // Today item - same day as test date (May 15, 2023)
      {
        id: 'today',
        title: 'Today item',
        createdTimestamp: '2023-05-15T12:00:00.000Z', // Same day, noon UTC
        options: [], // Empty array instead of empty object
      },

      // Yesterday item (May 14, 2023)
      {
        id: 'yesterday',
        title: 'Yesterday item',
        createdTimestamp: '2023-05-14T12:00:00.000Z',
        options: [],
      },

      // Week item (May 10, 2023) - within 7 days but not yesterday
      {
        id: 'week',
        title: 'Week item',
        createdTimestamp: '2023-05-10T12:00:00.000Z',
        options: [],
      },

      // Month item (April 20, 2023) - within 30 days but not within 7 days
      {
        id: 'month',
        title: 'Month item',
        createdTimestamp: '2023-04-20T12:00:00.000Z',
        options: [],
      },

      // Old item (March 1, 2023) - older than 30 days
      {
        id: 'old',
        title: 'Old item',
        createdTimestamp: '2023-03-01T12:00:00.000Z',
        options: [],
      },
    ]
  })

  it('should categorize items correctly based on their creation date', () => {
    // Create a version of the test that uses our test date as the reference date
    const categorized = categorizeHistoryItems(items, standardConfig, testDate)

    // Verify categorization using title instead of id
    expect(categorized.today.length).toBe(1)
    expect(categorized.today[0].title).toBe('Today item')

    expect(categorized.yesterday.length).toBe(1)
    expect(categorized.yesterday[0].title).toBe('Yesterday item')

    expect(categorized.previous7Days.length).toBe(1)
    expect(categorized.previous7Days[0].title).toBe('Week item')

    expect(categorized.previous30Days.length).toBe(1)
    expect(categorized.previous30Days[0].title).toBe('Month item')

    expect(categorized.olderItems.length).toBe(1)
    expect(categorized.olderItems[0].title).toBe('Old item')
  })

  it('should handle empty history items array', () => {
    const categorized = categorizeHistoryItems([], standardConfig, testDate)

    expect(categorized.today).toEqual([])
    expect(categorized.yesterday).toEqual([])
    expect(categorized.previous7Days).toEqual([])
    expect(categorized.previous30Days).toEqual([])
    expect(categorized.olderItems).toEqual([])
  })

  it('should work with custom date ranges', () => {
    const customConfig: IDateRangeConfig = {
      today: true,
      yesterday: false,
      previousDays: [14],
      customRanges: [{ name: 'quarterAgo', daysAgo: 90 }],
    }

    // Create specific items for this test
    const customItems: HistoryItemType[] = [
      // Today item
      {
        id: 'today',
        title: 'Today item',
        createdTimestamp: '2023-05-15T12:00:00.000Z',
        options: [],
      },

      // Two weeks item (May 5, 2023) - within 14 days
      {
        id: 'two-weeks',
        title: 'Two weeks item',
        createdTimestamp: '2023-05-05T12:00:00.000Z',
        options: [],
      },

      // Quarter item (March 15, 2023) - within 90 days
      {
        id: 'quarter',
        title: 'Quarter item',
        createdTimestamp: '2023-03-15T12:00:00.000Z',
        options: [],
      },

      // Old item (January 1, 2023) - older than 90 days
      {
        id: 'old',
        title: 'Old item',
        createdTimestamp: '2023-01-01T12:00:00.000Z',
        options: [],
      },
    ]

    const categorized = categorizeHistoryItems(customItems, customConfig, testDate)

    // Test custom configuration results using title instead of id
    expect(categorized.today.length).toBe(1)
    expect(categorized.today[0].title).toBe('Today item')

    // No yesterday category in this config
    expect(categorized.yesterday).toBeUndefined()

    expect(categorized.previous14Days.length).toBe(1)
    expect(categorized.previous14Days[0].title).toBe('Two weeks item')

    expect(categorized.quarterAgo.length).toBe(1)
    expect(categorized.quarterAgo[0].title).toBe('Quarter item')

    expect(categorized.olderItems.length).toBe(1)
    expect(categorized.olderItems[0].title).toBe('Old item')
  })
})
