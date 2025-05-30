<script lang="ts">
  import { goto } from '$app/navigation'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import { page } from '$app/state'

  let { children } = $props()

  let urlFirstDirectory = $derived.by(() => {
    const segments = page.url.pathname.split('/').filter(Boolean)
    return segments.length > 0 ? `/${segments[1]}` : '/'
  })

  const isActive = (path: string) => path === urlFirstDirectory
</script>

<div class="flex h-screen bg-base-200">
  <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 max-md:!w-0">
    <SidebarMenu title="Assistant">
      <div class="flex flex-col h-full gap-2">
        <button type="button" class="btn btn-sm {isActive('/zoo') ? 'btn-neutral' : 'btn-ghost'}"
                onclick={() => goto('/assistant/zoo')}>
          <span class="text-s">Assistant Zoo</span>
        </button>
        <button type="button" class="btn btn-sm {isActive('/edit') ? 'btn-neutral' : 'btn-ghost'}"
                onclick={() => goto('/assistant/edit')}>
          <span class="text-s">Your assistants</span>
        </button>
      </div>
    </SidebarMenu>
  </aside>
  <main class="m-2 flex-grow rounded-lg border bg-stone-50 overflow-hidden">
    {@render children()}
  </main>
</div>
