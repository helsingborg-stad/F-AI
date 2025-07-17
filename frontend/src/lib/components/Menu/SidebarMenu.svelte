<script lang="ts">
  import type { Snippet } from 'svelte'

  interface Props {
    children?: Snippet
  }

  const { children }: Props = $props()
</script>

<nav class="h-full flex flex-col pl-1">
  <div class="flex flex-col gap-2 h-full overflow-y-auto">
    {#if children}
      {@render children()}
    {/if}
  </div>
</nav>
