<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import Avatar from '$lib/components/Navbar/Avatar.svelte'

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

<nav class="navbar p-0 min-h-0">
  <div class="grow md:grow-0">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-circle btn-ghost md:hidden">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h7"
          />
        </svg>
      </div>
      <ul class="menu dropdown-content z-10 mt-3 w-52 gap-3 bg-base-200 p-2 shadow">
        {#each navbarMenu as { label, path }}
          <li><a href={path} class:active={isActive(path)}>{label}</a></li>
        {/each}
      </ul>
    </div>
    <div class="grow">
      {#if navbarTitle}
        <span>{navbarTitle}</span>
      {/if}
    </div>
  </div>
  <div class="hidden grow justify-end md:flex">
    <ul class="menu menu-horizontal gap-1">
      {#each navbarMenu as { label, path }}
        <li><a href={path} class:active={isActive(path)}>{label}</a></li>
      {/each}
    </ul>
  </div>
  <Avatar {avatarUrl} {avatarPlaceholder} menuItems={avatarMenu} />
</nav>
