<script lang="ts">
  import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte'
  import type { HistoryItemType } from '$lib/types.js'
  import type { IDateRangeConfig } from '$lib/utils/dates.js'
  import {
    categorizeHistoryItems,
    getCategoryTitles,
  } from '$lib/components/Menu/Chat/HistoryTree/historyUtils.js'

  interface Props {
    items: HistoryItemType[],
    highlightedIds: string[],
    onClick: (id: string) => void,
    dateRangeConfig?: IDateRangeConfig
  }

  let {
    items,
    highlightedIds,
    onClick,
    dateRangeConfig = {
      today: true,
      yesterday: true,
      previousDays: [7, 30],
    },
  }: Props = $props()

  // Get category titles based on configuration
  let categoryTitles = $derived(getCategoryTitles(dateRangeConfig))

  // Categorize history items
  let categorizedItems = $derived(categorizeHistoryItems(items, dateRangeConfig))
</script>

<div class="rounded-box flex flex-col gap-1">
  {#each Object.keys(categorizedItems) as category}
    {#if categorizedItems[category].length > 0}
      <p class="font-bold">
        {categoryTitles[category] || category}
      </p>
      {#each categorizedItems[category] as item(item.id)}
        <HistoryItem
          title={item.title}
          highlighted={highlightedIds.includes(item.id)}
          options={item.options}
          onClick={() => onClick(item.id)}
        />
      {/each}
    {/if}
  {/each}
</div>
