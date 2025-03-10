<script lang="ts">
  import { page } from '$app/state'

  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte'

  let { children } = $props()

  const navBarItems = [
    { label: 'Chat', path: '/chat' },
    { label: 'Settings', path: '/settings' },
  ]

  const menuSidebarItems = []

  const urlFirstDirectory = $derived(() => {
    const segments = page.url.pathname.split('/').filter(Boolean)
    return segments.length > 0 ? `/${segments[0]}` : '/'
  })

  // TODO: Duplicate code, use single instance of code
  const navbarTitle = $derived(() => {
    const matchingItem = navBarItems.find((item) => item.path === urlFirstDirectory())
    return matchingItem ? matchingItem.label : 'Folkets AI'
  })
</script>

<div class="flex flex-grow bg-base-200">
  <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 max-md:!w-0">
    <MenuSidebar
      menuSidebarTitle={navbarTitle()}
      {menuSidebarItems}
      currentUrlPath={page.url.pathname}
    />
  </aside>
  <main class="m-2 flex-grow rounded-lg border bg-stone-50">
    {@render children()}
  </main>
</div>
