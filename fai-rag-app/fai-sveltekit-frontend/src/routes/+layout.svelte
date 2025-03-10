<script lang="ts">
  import '../app.css'
  import { page } from '$app/state'

  import Navbar from '$lib/components/Navbar/Navbar.svelte'

  let { children } = $props()

  const NAVBAR_TITLE = 'Folkets AI'

  const navBarItems = [
    { label: 'Chat', path: '/chat' },
    { label: 'Settings', path: '/settings' },
  ]
</script>

<!--
Root layout component
This layout file is responsible for setting the Navbar for the application
and providing the main content area for child components.
-->
<div class="flex h-screen flex-col">
  <header class="flex w-full bg-base-200 md:px-4">
    <Navbar navbarTitle={NAVBAR_TITLE} {navBarItems} currentUrlPath={page.url.pathname} />
  </header>
  <div class="flex flex-grow">
    <main class="flex h-full flex-grow flex-col">
      {@render children()}
    </main>
  </div>
</div>
