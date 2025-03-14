<script lang="ts">
  import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte'
  import type { HistoryItemType } from '$lib/types.js'
  import type { IDateRangeConfig } from '$lib/utils/dates.js'
  import {
    categorizeHistoryItems,
    getCategoryTitles,
  } from '$lib/components/Menu/Chat/HistoryTree/historyUtils.js'

  interface Props {
    historyItems: HistoryItemType[],
    dateRangeConfig: IDateRangeConfig
  }

  let {
    historyItems = [],
    dateRangeConfig = {
      today: true,
      yesterday: true,
      previousDays: [7, 30]
    }
  }: Props = $props()

  // Get category titles based on configuration
  let categoryTitles = $derived(getCategoryTitles(dateRangeConfig))

  // Categorize history items
  let categorizedItems = $derived(categorizeHistoryItems(historyItems, dateRangeConfig))
</script>

<div class="rounded-box">
  {#each Object.keys(categorizedItems) as category}
    {#if categorizedItems[category].length > 0}
      <p>
        {categoryTitles[category] || category}
      </p>
      {#each categorizedItems[category] as item}
        <HistoryItem title={item.title} itemOptions={item.itemOptions} />
      {/each}
    {/if}
  {/each}
</div>
