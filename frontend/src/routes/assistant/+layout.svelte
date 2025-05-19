<script>
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'

  let { children } = $props()
</script>

<div class="flex h-screen bg-base-200">
  <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 max-md:!w-0">
    <SidebarMenu title="Assistant" />
  </aside>
  <main class="m-2 flex-grow rounded-lg border bg-stone-50 overflow-hidden">
    {@render children()}
  </main>
</div>