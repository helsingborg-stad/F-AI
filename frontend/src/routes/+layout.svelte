<script lang="ts">
  import '../app.css'
  import { page } from '$app/state'

  import Navbar from '$lib/components/Navbar/Navbar.svelte'
  import { hasScope, setUser } from '$lib/state/user.svelte.js'

  let { children, data } = $props()

  setUser(data.user)

  const NAVBAR_TITLE = 'Folkets AI'

  const navBarItems = [
    { label: 'Chat', path: '/chat' },
    { label: 'Assistants', path: '/assistant' },
  ]

  if (hasScope('settings.read')) {
    navBarItems.push({ label: 'Settings', path: '/settings' })
  }

  let showNavbar = $derived(!page.url.pathname.startsWith('/login'))
</script>

<!--
Root layout component
This layout file is responsible for setting the Navbar for the application
and providing the main content area for child components.
-->
<div class="flex h-screen flex-col">
  {#if showNavbar}
    <header class="flex w-full bg-base-200 md:px-4">
      <Navbar navbarTitle={NAVBAR_TITLE} {navBarItems} currentUrlPath={page.url.pathname} />
    </header>
  {/if}
  <div class="flex flex-grow">
    <main class="flex h-full flex-grow flex-col">
      {@render children()}
    </main>
  </div>
</div>
