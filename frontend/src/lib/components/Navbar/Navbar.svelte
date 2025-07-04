<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import Avatar from '$lib/components/Navbar/Avatar.svelte'
  import NavbarMenu from '$lib/components/Menu/Navbar/NavbarMenu.svelte'

  interface Props {
    navbarTitle: string
    avatarUrl?: URL
    navbarMenu: IMenuItem[]
    currentUrlPath: string
    avatarPlaceholder: string
    avatarMenu: {
      title: string,
      action: string
    }[]
  }

  let { navbarTitle, avatarUrl, navbarMenu, currentUrlPath, avatarPlaceholder, avatarMenu }: Props = $props()

  let urlFirstDirectory = $derived.by(() => {
    const segments = currentUrlPath.split('/').filter(Boolean)
    return segments.length > 0 ? `/${segments[0]}` : '/'
  })

  const isActive = (path: string) => path === urlFirstDirectory
</script>

<nav class="navbar py-0 min-h-0">

  <div class="ml-2 grow md:grow-0">
    {#if navbarTitle}
      <span>{navbarTitle}</span>
    {/if}
  </div>

  <div class="hidden grow justify-end md:flex">
    <ul class="menu menu-horizontal gap-1">
      {#each navbarMenu as { label, path }}
        <li><a href={path} class:active={isActive(path)}>{label}</a></li>
      {/each}
    </ul>
  </div>

  <div class="hidden md:flex md:flex-none">
    <Avatar {avatarUrl} {avatarPlaceholder} menuItems={avatarMenu} />
  </div>

  <div class="md:hidden">
    <NavbarMenu {navbarMenu} {isActive} />
  </div>

</nav>
