<script lang="ts">
  import MenuHeader from '$lib/components/Menu/MenuHeader.svelte'
  import type { Snippet } from 'svelte'

  interface Props {
    title: string
    children?: Snippet
  }

  const { title, children }: Props = $props()
</script>

<nav class="h-full flex flex-col">
  <MenuHeader iconName="panelLeft" {title} />
  <div class="flex flex-col gap-2 overflow-y-scroll">
    {#if children}
      {@render children()}
    {/if}
  </div>
</nav>
