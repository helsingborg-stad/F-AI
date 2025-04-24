<script>
  import { page } from '$app/state'
  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte'

  let { children } = $props()

  const menuSidebarItems = [{ label: 'Assistant zoo', path: '/assistant' }]
</script>

<div class="flex flex-grow bg-base-200">
  <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 max-md:!w-0">
    <MenuSidebar
      menuSidebarTitle="Assistant"
      {menuSidebarItems}
      currentUrlPath={page.url.pathname}
    />
  </aside>
  <main class="m-2 flex-grow rounded-lg border bg-stone-50">
    {@render children()}
  </main>
</div>
