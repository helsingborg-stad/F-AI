<script lang="ts">
  import HistoryItemOptions from '$lib/components/Menu/Chat/HistoryItemOptions.svelte';
  import { icons } from '$lib/components/Icon/icons.js';

  export let title: string;
  export let itemOptions: { iconName: keyof typeof icons, title: string, onClick: () => void }[] = [];
</script>

<div class="relative group/item flex items-center px-4 py-2 hover:bg-gray-100 rounded-md">
  <span class="flex-1 truncate pr-8">{title}</span>
  {#if itemOptions.length > 0}
    <div class="dropdown dropdown-end group/edit invisible group-hover/item:visible">
      <button class="btn btn-sm btn-ghost" aria-label="Edit">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-ellipsis"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
      </button>
      <ul class="menu dropdown-content bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
        {#each itemOptions as option}
          <HistoryItemOptions
          iconName={option.iconName}
          title={option.title}
          onClick={option.onClick} />
        {/each}
      </ul>
    </div>
  {/if}
</div>