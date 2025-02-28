import { describe, it, expect } from 'vitest'
import {
  getDateBoundaries,
  getDaysAgo,
  getStartOfDay,
  isDateInRange,
} from '$lib/utils/dates.js'

describe('Date utility functions', () => {
  // Use a fixed reference date and Date constructor with explicit parts to avoid timezone issues
  const referenceDate = new Date(2023, 4, 15, 14, 30, 45, 123) // 2023-05-15, 14:30:45.123

  describe('getStartOfDay', () => {
    it('should set time to midnight (00:00:00.000)', () => {
      const result = getStartOfDay(referenceDate)

      // Check that date components are preserved
      expect(result.getFullYear()).toBe(2023)
      expect(result.getMonth()).toBe(4) // May is month 4 (zero-based)
      expect(result.getDate()).toBe(15)

      // Check that time is reset to midnight
      expect(result.getHours()).toBe(0)
      expect(result.getMinutes()).toBe(0)
      expect(result.getSeconds()).toBe(0)
      expect(result.getMilliseconds()).toBe(0)
    })

    it('should properly normalize the time to midnight', () => {
      // Create a date with a specific time
      const dateWithTime = new Date('2023-05-15T23:30:00Z')
      const result = getStartOfDay(dateWithTime)

      // The date component should be preserved
      expect(result.getDate()).toBe(dateWithTime.getDate())

      // The time should be set to midnight
      expect(result.getHours()).toBe(0)
      expect(result.getMinutes()).toBe(0)
      expect(result.getSeconds()).toBe(0)
      expect(result.getMilliseconds()).toBe(0)
    })

    it('should preserve the same date when converting to start of day', () => {
      // Test with multiple dates to ensure consistent behavior
      const testCases = [
        new Date('2023-05-15T12:30:45Z'),
        new Date('2023-05-15T23:59:59Z'),
        new Date('2023-05-15T00:00:01Z'),
      ]

      testCases.forEach((date) => {
        const localDay = date.getDate()
        const result = getStartOfDay(date)

        // The local date should remain the same
        expect(result.getDate()).toBe(localDay)
      })
    })

    it('should create a new Date instance without modifying the original', () => {
      const original = new Date(referenceDate)
      const result = getStartOfDay(original)

      expect(result).not.toBe(original)
      expect(original.getHours()).toBe(14)
    })
  })

  describe('getDaysAgo', () => {
    it('should return a date N days before the provided date', () => {
      // Test with different day offsets
      const oneDayAgo = getDaysAgo(referenceDate, 1)
      const sevenDaysAgo = getDaysAgo(referenceDate, 7)
      const thirtyDaysAgo = getDaysAgo(referenceDate, 30)

      expect(oneDayAgo.getDate()).toBe(14) // 15 - 1
      expect(oneDayAgo.getMonth()).toBe(4) // Still May

      expect(sevenDaysAgo.getDate()).toBe(8) // 15 - 7
      expect(sevenDaysAgo.getMonth()).toBe(4) // Still May

      // May 15 - 30 days = April 15
      expect(thirtyDaysAgo.getDate()).toBe(15)
      expect(thirtyDaysAgo.getMonth()).toBe(3) // April is month 3
    })

    it('should handle month and year boundaries correctly', () => {
      // Test crossing month boundary
      const startOfMonth = new Date('2023-05-01T12:00:00Z')
      const endOfPrevMonth = getDaysAgo(startOfMonth, 1)

      expect(endOfPrevMonth.getDate()).toBe(30) // April 30th
      expect(endOfPrevMonth.getMonth()).toBe(3) // April

      // Test crossing year boundary
      const startOfYear = new Date('2023-01-01T12:00:00Z')
      const endOfPrevYear = getDaysAgo(startOfYear, 1)

      expect(endOfPrevYear.getDate()).toBe(31) // December 31st
      expect(endOfPrevYear.getMonth()).toBe(11) // December
      expect(endOfPrevYear.getFullYear()).toBe(2022)
    })

    it('should set the time to midnight', () => {
      const result = getDaysAgo(referenceDate, 5)

      expect(result.getHours()).toBe(0)
      expect(result.getMinutes()).toBe(0)
      expect(result.getSeconds()).toBe(0)
      expect(result.getMilliseconds()).toBe(0)
    })

    describe('isDateInRange', () => {
      it('should return true when date is after startDate with no endDate', () => {
        const startDate = new Date('2023-05-10T00:00:00Z')
        const date = new Date('2023-05-15T12:30:45Z')

        expect(isDateInRange(date, startDate)).toBe(true)
      })

      it('should return false when date is before startDate with no endDate', () => {
        const startDate = new Date('2023-05-20T00:00:00Z')
        const date = new Date('2023-05-15T12:30:45Z')

        expect(isDateInRange(date, startDate)).toBe(false)
      })

      it('should return true when date is exactly on startDate with no endDate', () => {
        const startDate = new Date('2023-05-15T00:00:00Z')
        const date = new Date('2023-05-15T00:00:00Z')

        expect(isDateInRange(date, startDate)).toBe(true)
      })

      it('should return true when date is between startDate and endDate', () => {
        const startDate = new Date('2023-05-10T00:00:00Z')
        const endDate = new Date('2023-05-20T00:00:00Z')
        const date = new Date('2023-05-15T12:30:45Z')

        expect(isDateInRange(date, startDate, endDate)).toBe(true)
      })

      it('should return true when date is exactly on startDate with endDate', () => {
        const startDate = new Date('2023-05-15T00:00:00Z')
        const endDate = new Date('2023-05-20T00:00:00Z')
        const date = new Date('2023-05-15T00:00:00Z')

        expect(isDateInRange(date, startDate, endDate)).toBe(true)
      })

      it('should return false when date is on or after endDate', () => {
        const startDate = new Date('2023-05-10T00:00:00Z')
        const endDate = new Date('2023-05-15T00:00:00Z')
        const onEndDate = new Date('2023-05-15T00:00:00Z')
        const afterEndDate = new Date('2023-05-16T00:00:00Z')

        expect(isDateInRange(onEndDate, startDate, endDate)).toBe(false)
        expect(isDateInRange(afterEndDate, startDate, endDate)).toBe(false)
      })
    })

    describe('getDateBoundaries', () => {
      it('should return correct date boundaries based on reference date', () => {
        // Use a specific reference date for testing
        const referenceDate = new Date(2023, 4, 15, 12, 0, 0) // May 15, 2023, 12:00:00

        const boundaries = getDateBoundaries(referenceDate)

        // Today should be 2023-05-15 00:00:00
        expect(boundaries.today.getFullYear()).toBe(2023)
        expect(boundaries.today.getMonth()).toBe(4) // May (0-indexed)
        expect(boundaries.today.getDate()).toBe(15)
        expect(boundaries.today.getHours()).toBe(0)

        // Yesterday should be 2023-05-14 00:00:00
        expect(boundaries.yesterday.getFullYear()).toBe(2023)
        expect(boundaries.yesterday.getMonth()).toBe(4)
        expect(boundaries.yesterday.getDate()).toBe(14)

        // Previous 7 days should be 2023-05-08 00:00:00
        expect(boundaries.previousSevenDays.getFullYear()).toBe(2023)
        expect(boundaries.previousSevenDays.getMonth()).toBe(4)
        expect(boundaries.previousSevenDays.getDate()).toBe(8)

        // Previous 30 days should be 2023-04-15 00:00:00
        expect(boundaries.previousThirtyDays.getFullYear()).toBe(2023)
        expect(boundaries.previousThirtyDays.getMonth()).toBe(3) // April
        expect(boundaries.previousThirtyDays.getDate()).toBe(15)
      })

      it('should use current date when no reference date is provided', () => {
        const now = new Date()
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())

        const boundaries = getDateBoundaries()

        // Check that today's date matches the current date
        expect(boundaries.today.getFullYear()).toBe(today.getFullYear())
        expect(boundaries.today.getMonth()).toBe(today.getMonth())
        expect(boundaries.today.getDate()).toBe(today.getDate())
        expect(boundaries.today.getHours()).toBe(0)
        expect(boundaries.today.getMinutes()).toBe(0)
        expect(boundaries.today.getSeconds()).toBe(0)
      })
    })
  })
})
