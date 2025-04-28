<script lang="ts">
  import type { Snippet } from 'svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    toolTip: string
    children?: Snippet
  }

  let { toolTip, children }: Props = $props()
</script>

<div class="tooltip" data-tip={toolTip}>
  <div class="flex flex-row gap-2 items-center">
    {#if children}
      {@render children()}
    {/if}
    <div class="flex-shrink-0">
      <Icon icon={icons["info"]} width={14} height={14} />
    </div>
  </div>
</div>
