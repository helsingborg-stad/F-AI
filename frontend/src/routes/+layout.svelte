<script lang="ts">
  import '../app.css'
  import { page } from '$app/state'

  import Navbar from '$lib/components/Navbar/Navbar.svelte'
  import { userState } from '$lib/state/user.svelte.js'

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
<div class="flex h-screen flex-col">
  {#if showNavbar}
    <header class="flex w-full bg-base-200 md:px-4">
      <Navbar
        navbarTitle={navbarData.title}
        navbarMenu={navbarData.navbarMenu}
        currentUrlPath={page.url.pathname}
        {avatarPlaceholder}
        avatarMenu={data.avatarMenu}
      />
    </header>
  {/if}
  <div class="flex flex-grow">
    <main class="flex h-full flex-grow flex-col">
      {@render children()}
    </main>
  </div>
</div>
