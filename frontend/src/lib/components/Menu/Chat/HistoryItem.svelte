<script lang="ts">
  import HistoryItemOptions from '$lib/components/Menu/Chat/HistoryItemOptions.svelte'
  import type { ItemOptionsType } from '$lib/types.js'

  interface Props {
    title: string,
    highlighted: boolean,
    options: ItemOptionsType[],
    onClick: () => void,
  }

  let {
    title,
    highlighted,
    options,
    onClick,
  }: Props = $props()
</script>

<div
  class="group/item w-full max-w-full flex px-2 py-1 rounded-md hover:bg-gray-200 active:bg-gray-300"
  class:bg-gray-300={highlighted}
>
  <button
    class="grow truncate text-left pr-2"
    title={title}
    onclick={onClick}
  >
    <span>{title}</span>
  </button>
  {#if options.length > 0}
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
        >
          <circle cx="12" cy="12" r="1" />
          <circle cx="19" cy="12" r="1" />
          <circle
            cx="5"
            cy="12"
            r="1"
          />
        </svg
        >
      </button>
      <ul class="menu dropdown-content z-[1] w-52 rounded-box bg-base-100 p-2 shadow">
        {#each options as option}
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
