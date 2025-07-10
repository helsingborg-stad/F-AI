<script lang="ts">
  import '../app.css'
  import { page } from '$app/state'

  import Navbar from '$lib/components/Navbar/Navbar.svelte'
  import { userState } from '$lib/state/user.svelte.js'
  import SidebarProvider from '$lib/providers/SidebarProvider.svelte'

  let { children, data } = $props()

  const navbarData = data.navbar

  let showNavbar = $derived(!page.url.pathname.startsWith('/login'))

  let avatarPlaceholder = $derived.by(() => {
    return userState.email ? userState.email : ''
  })
</script>

<!--
Root layout component
This layout file is responsible for setting the Navbar for the application
and providing the main content area for child components.
-->
<SidebarProvider>
  <div class="flex flex-col min-h-screen h-screen max-h-screen overflow-hidden">
    {#if showNavbar}
      <header class="w-full bg-base-200 md:px-4">
        <Navbar
          navbarTitle={navbarData.title}
          navbarMenu={navbarData.navbarMenu}
          currentUrlPath={page.url.pathname}
          {avatarPlaceholder}
          avatarMenu={data.avatarMenu}
        />
      </header>
    {/if}
    <div class="flex-grow overflow-hidden">
      <main class="h-full">
        {@render children()}
      </main>
    </div>
  </div>
</SidebarProvider>
