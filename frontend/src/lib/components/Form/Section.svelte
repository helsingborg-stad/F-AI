<script lang="ts">
  import type { Snippet } from 'svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'

  interface Props {
    title: string;
    children: Snippet
  }

  let { title, children }: Props = $props()
</script>

<div class="pt-5 space-y-2">
  <div class="opacity-50 pb-1">{title}</div>
  <HorizontalDivider />
  {@render children()}
</div>