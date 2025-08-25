<script lang="ts">
  import type { Snippet } from 'svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'

  interface Props {
    title: string
    children: Snippet
  }

  let { title, children }: Props = $props()
</script>

<div class="space-y-2 pt-5">
  <div class="pb-1 opacity-50">{title}</div>
  <HorizontalDivider />
  {@render children()}
</div>
