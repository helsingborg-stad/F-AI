<script lang="ts">
  import type { Snippet } from 'svelte'

  interface Props {
    children?: Snippet
  }

  const { children }: Props = $props()
</script>

<nav class="flex h-full flex-col pl-1">
  <div class="flex h-full flex-col gap-2 overflow-y-auto">
    {#if children}
      {@render children()}
    {/if}
  </div>
</nav>
