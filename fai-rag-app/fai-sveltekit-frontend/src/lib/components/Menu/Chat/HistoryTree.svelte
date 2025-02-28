<script lang="ts">
  import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte'
  import type { HistoryItemType } from '$lib/types.js'
  import { getDateBoundaries, isDateInRange } from '$lib/utils/dates.js'

  export let historyItems: HistoryItemType[] = []

  // Get date boundaries for categorization
  const dateRanges = getDateBoundaries()

  type HistoryCategorized = {
    todaysHistory: HistoryItemType[]
    yesterdaysHistory: HistoryItemType[]
    previousSevenDays: HistoryItemType[]
    previousThirtyDays: HistoryItemType[]
    olderItems: HistoryItemType[]
  }

  /**
   * Function to categorize history items into time periods
   */
  function categorizeHistoryItems(items: HistoryItemType[]): HistoryCategorized {
    return items.reduce<HistoryCategorized>(
      (categories, item) => {
        const createdDate = item.created

        // Determine which category this item belongs to
        if (isDateInRange(createdDate, dateRanges.today)) {
          categories.todaysHistory.push(item)
        } else if (isDateInRange(createdDate, dateRanges.yesterday, dateRanges.today)) {
          categories.yesterdaysHistory.push(item)
        } else if (
          isDateInRange(createdDate, dateRanges.previousSevenDays, dateRanges.yesterday)
        ) {
          categories.previousSevenDays.push(item)
        } else if (
          isDateInRange(
            createdDate,
            dateRanges.previousThirtyDays,
            dateRanges.previousSevenDays,
          )
        ) {
          categories.previousThirtyDays.push(item)
        } else {
          categories.olderItems.push(item)
        }

        return categories
      },
      {
        todaysHistory: [],
        yesterdaysHistory: [],
        previousSevenDays: [],
        previousThirtyDays: [],
        olderItems: [],
      },
    )
  }

  const {
    todaysHistory,
    yesterdaysHistory,
    previousSevenDays,
    previousThirtyDays,
    olderItems,
  } = categorizeHistoryItems(historyItems)
</script>

<div class="rounded-box">
  {#if todaysHistory.length > 0}
    <p>Today</p>
    {#each todaysHistory as item}
      <HistoryItem title={item.title} itemOptions={item.itemOptions} />
    {/each}
  {/if}

  {#if yesterdaysHistory.length > 0}
    <p>Yesterday</p>
    {#each yesterdaysHistory as item}
      <HistoryItem title={item.title} itemOptions={item.itemOptions} />
    {/each}
  {/if}

  {#if previousSevenDays.length > 0}
    <p>Previous 7 days</p>
    {#each previousSevenDays as item}
      <HistoryItem title={item.title} itemOptions={item.itemOptions} />
    {/each}
  {/if}

  {#if previousThirtyDays.length > 0}
    <p>Last 30 days</p>
    {#each previousThirtyDays as item}
      <HistoryItem title={item.title} itemOptions={item.itemOptions} />
    {/each}
  {/if}

  {#if olderItems.length > 0}
    <p>Older items</p>
    {#each olderItems as item}
      <HistoryItem title={item.title} itemOptions={item.itemOptions} />
    {/each}
  {/if}
</div>
