<script lang="ts">
  import { uiState } from '$lib/state/ui.svelte.js'
  import type { Snippet } from 'svelte'

  interface Props {
    children: Snippet
  }

  const { children }: Props = $props()

  $effect(() => {
    let resizeTimer: number

    const handleResize = () => {
      clearTimeout(resizeTimer)
      resizeTimer = setTimeout(() => {
        const isMobile = window.innerWidth < 768
        uiState.setShowSidebarAuto(!isMobile)
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

{#if uiState.showSidebar}
  <button
    type="button"
    aria-label="Close sidebar"
    class="fixed inset-0 z-[30] bg-transparent cursor-default p-0 border-0 md:hidden"
    onclick={() => uiState.setShowSidebarManual(false)}
  ></button>
{/if}

<aside
  class="w-60 flex-shrink-0 bg-base-200 max-md:absolute max-md:top-0 max-md:left-0 max-md:h-full max-md:z-[30] max-md:shadow-[2px_0_8px_rgba(0,0,0,0.15)] max-md:backdrop-blur"
  class:hidden={!uiState.showSidebar}
>
  {@render children()}
</aside>
