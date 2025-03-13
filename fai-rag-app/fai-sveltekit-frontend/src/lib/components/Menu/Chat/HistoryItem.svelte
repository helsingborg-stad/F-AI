<script lang="ts">
  import HistoryItemOptions from '$lib/components/Menu/Chat/HistoryItemOptions.svelte'
  import type { ItemOptionsType } from '$lib/types.js'

  interface Props {
    title: string,
    itemOptions: ItemOptionsType[]
  }

  let {
    title,
    itemOptions = []
  }: Props = $props()
</script>

<div
  class="group/item relative flex items-center rounded-md px-4 py-1.5 hover:bg-gray-100"
>
  <span class="flex-1 truncate pr-8">{title}</span>
  {#if itemOptions.length > 0}
    <div class="group/edit dropdown dropdown-end invisible group-hover/item:visible">
      <button class="btn btn-ghost btn-sm" aria-label="Edit">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-ellipsis"
          ><circle cx="12" cy="12" r="1" /><circle cx="19" cy="12" r="1" /><circle
            cx="5"
            cy="12"
            r="1"
          /></svg
        >
      </button>
      <ul class="menu dropdown-content z-[1] w-52 rounded-box bg-base-100 p-2 shadow">
        {#each itemOptions as option}
          <HistoryItemOptions
            iconName={option.iconName}
            title={option.title}
            onClick={option.onClick}
          />
        {/each}
      </ul>
    </div>
  {/if}
</div>
