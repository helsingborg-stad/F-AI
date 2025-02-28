import { describe, it, expect, beforeEach } from 'vitest'
import { getCategoryTitles, categorizeHistoryItems } from '$lib/utils/historyUtils.js'
import type { HistoryItemType } from '$lib/types.js'
import type { DateRangeConfig } from '$lib/utils/dates.js'

// Create a test-specific interface that extends DateRangeConfig
interface TestDateRangeConfig extends DateRangeConfig {
  _testDate?: Date
}

describe('getCategoryTitles', () => {
  it('should return default category titles', () => {
    const config: DateRangeConfig = {
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
    const config: DateRangeConfig = {
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

  const standardConfig: TestDateRangeConfig = {
    today: true,
    yesterday: true,
    previousDays: [7, 30],
    _testDate: testDate,
  }

  beforeEach(() => {
    items = [
      // Today item - same day as test date (May 15, 2023)
      {
        title: 'Today item',
        created: new Date('2023-05-15T12:00:00.000Z'), // Same day, noon UTC
        itemOptions: [], // Empty array instead of empty object
      },

      // Yesterday item (May 14, 2023)
      {
        title: 'Yesterday item',
        created: new Date('2023-05-14T12:00:00.000Z'),
        itemOptions: [],
      },

      // Week item (May 10, 2023) - within 7 days but not yesterday
      {
        title: 'Week item',
        created: new Date('2023-05-10T12:00:00.000Z'),
        itemOptions: [],
      },

      // Month item (April 20, 2023) - within 30 days but not within 7 days
      {
        title: 'Month item',
        created: new Date('2023-04-20T12:00:00.000Z'),
        itemOptions: [],
      },

      // Old item (March 1, 2023) - older than 30 days
      {
        title: 'Old item',
        created: new Date('2023-03-01T12:00:00.000Z'),
        itemOptions: [],
      },
    ]
  })

  it('should categorize items correctly based on their creation date', () => {
    // Create a version of the test that uses our test date as the reference date
    const categorized = categorizeHistoryItems(items, standardConfig)

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
    const categorized = categorizeHistoryItems([], standardConfig)

    expect(categorized.today).toEqual([])
    expect(categorized.yesterday).toEqual([])
    expect(categorized.previous7Days).toEqual([])
    expect(categorized.previous30Days).toEqual([])
    expect(categorized.olderItems).toEqual([])
  })

  it('should work with custom date ranges', () => {
    const customConfig: TestDateRangeConfig = {
      today: true,
      yesterday: false,
      previousDays: [14],
      customRanges: [{ name: 'quarterAgo', daysAgo: 90 }],
      _testDate: testDate,
    }

    // Create specific items for this test
    const customItems: HistoryItemType[] = [
      // Today item
      {
        title: 'Today item',
        created: new Date('2023-05-15T12:00:00.000Z'),
        itemOptions: [],
      },

      // Two weeks item (May 5, 2023) - within 14 days
      {
        title: 'Two weeks item',
        created: new Date('2023-05-05T12:00:00.000Z'),
        itemOptions: [],
      },

      // Quarter item (March 15, 2023) - within 90 days
      {
        title: 'Quarter item',
        created: new Date('2023-03-15T12:00:00.000Z'),
        itemOptions: [],
      },

      // Old item (January 1, 2023) - older than 90 days
      {
        title: 'Old item',
        created: new Date('2023-01-01T12:00:00.000Z'),
        itemOptions: [],
      },
    ]

    const categorized = categorizeHistoryItems(customItems, customConfig)

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
