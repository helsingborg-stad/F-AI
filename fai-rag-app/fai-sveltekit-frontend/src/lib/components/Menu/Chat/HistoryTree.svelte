<script lang="ts">
  import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte'
  import type { HistoryItemType } from '$lib/types.js'

  export let historyItems: HistoryItemType[] = []

  const isDateWithinRange = (date: Date, startDate: Date, endDate: Date): boolean => {
    return date.getTime() > startDate.getTime() && date.getTime() < endDate.getTime()
  }

  let todaysHistory: HistoryItemType[] = []
  let yesterdaysHistory: HistoryItemType[] = []
  let previousSevenDays: HistoryItemType[] = []
  let previousThirtyDays: HistoryItemType[] = []
  let olderItems: HistoryItemType[] = []

  const today = new Date()

  // Today's range
  const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  const todayEnd = new Date(todayStart.getTime() + 24 * 60 * 60 * 1000)

  // Yesterday's range
  const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000)
  const yesterdayStart = new Date(
    yesterday.getFullYear(),
    yesterday.getMonth(),
    yesterday.getDate(),
  )
  const yesterdayEnd = new Date(yesterdayStart.getTime() + 24 * 60 * 60 * 1000)

  // Previous 7 days range
  const sevenDaysAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
  const sevenDaysStart = new Date(
    sevenDaysAgo.getFullYear(),
    sevenDaysAgo.getMonth(),
    sevenDaysAgo.getDate(),
  )
  const sevenDaysEnd = todayStart

  // Previous 30 days range
  const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
  const thirtyDaysStart = new Date(
    thirtyDaysAgo.getFullYear(),
    thirtyDaysAgo.getMonth(),
    thirtyDaysAgo.getDate(),
  )
  const thirtyDaysEnd = sevenDaysStart

  historyItems.forEach((item) => {
    const itemDate = item.created

    if (isDateWithinRange(itemDate, todayStart, todayEnd)) {
      todaysHistory.push(item)
    } else if (isDateWithinRange(itemDate, yesterdayStart, yesterdayEnd)) {
      yesterdaysHistory.push(item)
    } else if (isDateWithinRange(itemDate, sevenDaysStart, sevenDaysEnd)) {
      previousSevenDays.push(item)
    } else if (isDateWithinRange(itemDate, thirtyDaysStart, thirtyDaysEnd)) {
      previousThirtyDays.push(item)
    } else {
      olderItems.push(item)
    }
  })
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
