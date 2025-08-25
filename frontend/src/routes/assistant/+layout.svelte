<script lang="ts">
  import { goto } from '$app/navigation'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import { page } from '$app/state'
  import type { IMenuItem } from '$lib/types.js'
  import ResponsiveSidebar from '$lib/components/Menu/Chat/ResponsiveSidebar.svelte'

  let { data, children } = $props()
  const sidebarMenu: IMenuItem[] = data.sidebarMenu

  const isActive = (path: string) => path === page.url.pathname
</script>

<div class="relative flex h-full overflow-hidden bg-base-200">
  <ResponsiveSidebar>
    <SidebarMenu>
      <div class="flex h-full flex-col gap-2">
        {#each sidebarMenu as item}
          <button
            type="button"
            class="btn btn-sm {isActive(item.path) ? 'btn-neutral' : 'btn-ghost'}"
            onclick={() => goto(item.path)}
          >
            <span class="text-s">{item.label}</span>
          </button>
        {/each}
      </div>
    </SidebarMenu>
  </ResponsiveSidebar>
  <main class="m-2 flex-grow overflow-auto rounded-lg border bg-stone-50">
    {@render children()}
  </main>
</div>
