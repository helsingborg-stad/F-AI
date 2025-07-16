<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import type { IMenuItem } from '$lib/types.js'
  import Avatar from '$lib/components/Navbar/Avatar.svelte'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import { getSidebarContext } from '$lib/sidebar-context.js'

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

  const sidebarState = getSidebarContext()

  let urlFirstDirectory = $derived.by(() => {
    const segments = currentUrlPath.split('/').filter(Boolean)
    return segments.length > 0 ? `/${segments[0]}` : '/'
  })

  const isActive = (path: string) => path === urlFirstDirectory

  let isHovering = $state(false)

  let currentIcon = $derived.by(() => {
    if (isHovering) {
      return sidebarState.showSidebar ? icons["arrowLeftToLine"] : icons["arrowRightToLine"]
    }
    return icons["panelLeft"]
  })
</script>

<nav class="navbar py-0 min-h-0">
  <button
    class="btn btn-ghost btn-sm btn-square min-w-2 {sidebarState.showSidebar ? 'max-md:z-[40] max-md:relative' : ''}"
    onclick={sidebarState.toggleSidebar}
    onmouseenter={() => isHovering = true}
    onmouseleave={() => isHovering = false}
    aria-label={sidebarState.showSidebar ? m.nav_sidebar_hide_aria_label() : m.nav_sidebar_show_aria_label()}
  >
    <Icon icon={currentIcon} width={24} height={24} />
  </button>

  <div class="ml-2 grow">
    {#if navbarTitle}
      <span>{navbarTitle}</span>
    {/if}
  </div>

  <div class="grow justify-end flex">
    <ul class="menu menu-horizontal gap-1">
      {#each navbarMenu as { label, path }}
        <li><a href={path} class:active={isActive(path)}>{label}</a></li>
      {/each}
    </ul>
  </div>

  <div class="flex flex-none">
    <Avatar {avatarUrl} {avatarPlaceholder} menuItems={avatarMenu} />
  </div>
</nav>
