<!--TODO: Remove dropdown from navbar and place it in top `+layout.page`-->
<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    navbarTitle: string
    avatarUrl?: URL
    navBarItems: IMenuItem[]
    currentUrlPath: string
    avatarPlaceholder: string
  }

  let { navbarTitle, avatarUrl, navBarItems, currentUrlPath, avatarPlaceholder }: Props = $props()

  let urlFirstDirectory = $derived.by(() => {
    const segments = currentUrlPath.split('/').filter(Boolean)
    return segments.length > 0 ? `/${segments[0]}` : '/'
  })

  const isActive = (path: string) => path === urlFirstDirectory

  const getAvatarInitial = () => {
    return avatarPlaceholder.charAt(0).toUpperCase()
  }
</script>

<nav class="navbar">
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
        {#each navBarItems as { label, path }}
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
    <ul class="menu menu-horizontal gap-2">
      {#each navBarItems as { label, path }}
        <li><a href={path} class:active={isActive(path)}>{label}</a></li>
      {/each}
    </ul>
  </div>
  <div class="flex-none">
    {#if avatarUrl}
      <div class="avatar btn btn-circle btn-ghost">
        <div class="w-10 rounded-full">
          <img src={avatarUrl.toString()} alt="Profile" />
        </div>
      </div>
    {:else if avatarPlaceholder}
      <div class="avatar placeholder btn btn-circle btn-ghost">
        <div class="bg-neutral-300 text-base w-10 rounded-full">
          <span>{getAvatarInitial()}</span>
        </div>
      </div>
    {:else }
      <div class="avatar placeholder btn btn-circle btn-ghost">
        <div class="bg-neutral-300 w-10 rounded-full">
          <Icon icon={icons["circleUser"]} />
        </div>
      </div>
    {/if}
  </div>
</nav>
