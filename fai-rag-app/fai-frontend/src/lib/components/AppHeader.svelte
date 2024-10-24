<script lang="ts">
  import { type IRenderableComponent } from '../types'

  export let components: IRenderableComponent[] = []
</script>

<nav
  class="navbar sticky top-0 z-50 w-full border-b border-neutral border-opacity-25 bg-base-100 bg-opacity-40 px-0 tracking-tight backdrop-blur"
>
  <div class="w-full px-4">
    <div class="flex-1 lg:hidden lg:flex-none">
      <label for="my-drawer-2" aria-label="open sidebar" class="btn btn-square btn-ghost">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          class="inline-block h-6 w-6 stroke-current"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          ></path>
        </svg>
      </label>
    </div>
    <slot>
      {#each components as component}
        <svelte:component this={component.type} {...component.props} />
      {/each}
    </slot>
  </div>
</nav>
