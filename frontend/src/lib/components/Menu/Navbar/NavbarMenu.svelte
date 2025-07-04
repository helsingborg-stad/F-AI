<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'

  interface Props {
    navbarMenu: IMenuItem[]
    isActive: (path: string) => boolean
  }

  let { navbarMenu, isActive }: Props = $props()
</script>

<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="btn btn-circle btn-ghost">
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
