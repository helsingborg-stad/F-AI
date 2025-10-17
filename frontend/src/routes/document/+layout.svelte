<script lang="ts">
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import ResponsiveSidebar from '$lib/components/Menu/Chat/ResponsiveSidebar.svelte'

  import type { LayoutProps } from './$types.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { goto } from '$app/navigation'
  import { page } from '$app/state'

  let { data, children }: LayoutProps = $props()
  const { canEdit, collections } = data

  const activeId = $derived(page.params.collectionId)
</script>

<div class="relative flex h-full overflow-hidden bg-base-200">
  <ResponsiveSidebar>
    <SidebarMenu>
      <div class="flex h-full flex-col gap-2">
        <form method="POST" action="/document/?/createCollection" class="flex">
          <button type="submit" class="btn btn-neutral btn-sm grow" disabled={!canEdit}>
            <Icon icon={icons['plus']} width={16} height={16} />
            <span class="text-s">Create new collection</span>
          </button>
        </form>
        <div class="h-full overflow-y-auto pb-4 pl-2">
          <div class="flex flex-col gap-1 rounded-box">
            {#each collections as collection (collection.id)}
              <div
                class="group/item flex w-full max-w-full rounded-md px-2 py-1 hover:bg-gray-200 active:bg-gray-300"
                class:bg-gray-300={activeId === collection.id}
              >
                <button
                  class="grow truncate pr-2 text-left"
                  title="test"
                  onclick={() => goto(`/document/${collection.id}`)}
                >
                  <span>{collection.label}</span>
                </button>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </SidebarMenu>
  </ResponsiveSidebar>
  <div class="flex h-full w-full flex-col gap-2 overflow-hidden p-2 pt-0">
    <main class="h-full flex-grow overflow-hidden rounded-lg border bg-stone-50">
      {@render children()}
    </main>
  </div>
</div>
