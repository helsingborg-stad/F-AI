<script lang="ts">
  import '../app.css'
  import { page } from '$app/state'

  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte'
  import Navbar from '$lib/components/Navbar/Navbar.svelte'

  let { children } = $props()

  const NAVBAR_TITLE = 'Folkets AI'

  const navBarItems = [
    { label: 'Chat', path: '/chat' },
    { label: 'Settings', path: '/settings' },
  ]

  const menuSidebarItems = [
    { label: 'Home', path: '/' },
    { label: 'Chat', path: '/chat' },
    { label: 'Assistant', path: '/assistant' },
  ]
</script>

<div class="flex h-screen flex-col">
  <header class="flex w-full bg-base-200 md:px-4">
    <Navbar navbarTitle={NAVBAR_TITLE} {navBarItems} currentUrlPath={page.url.pathname} />
  </header>
  <div class="flex flex-grow">
    <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 max-md:!w-0">
      <MenuSidebar {menuSidebarItems} currentUrlPath={page.url.pathname} />
    </aside>
    <main class="flex-grow bg-stone-50">
      {@render children()}
    </main>
  </div>
</div>
