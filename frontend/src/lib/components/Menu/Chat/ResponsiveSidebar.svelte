<script lang="ts">
  import type { Snippet } from 'svelte'
  import { getSidebarContext } from '$lib/sidebar-context.js'

  interface Props {
    children: Snippet
  }

  const { children }: Props = $props()

  const sidebarState = getSidebarContext()

  $effect(() => {
    let resizeTimer: number

    const handleResize = () => {
      clearTimeout(resizeTimer)
      resizeTimer = setTimeout(() => {
        const isMobile = window.innerWidth < 768
        sidebarState.setShowSidebarAuto(!isMobile)
      }, 500)
    }

    handleResize()
    window.addEventListener('resize', handleResize)

    return () => {
      clearTimeout(resizeTimer)
      window.removeEventListener('resize', handleResize)
    }
  })
</script>

{#if sidebarState.showSidebar}
  <button
    type="button"
    aria-label="Close sidebar"
    class="fixed inset-0 z-[30] cursor-default border-0 bg-transparent p-0 md:hidden"
    onclick={() => sidebarState.setShowSidebarManual(false)}
  ></button>
{/if}

<aside
  class="w-60 flex-shrink-0 bg-base-200 max-md:absolute max-md:left-0 max-md:top-0 max-md:z-[30] max-md:h-full max-md:shadow-[2px_0_8px_rgba(0,0,0,0.15)] max-md:backdrop-blur"
  class:hidden={!sidebarState.showSidebar}
>
  {@render children()}
</aside>
