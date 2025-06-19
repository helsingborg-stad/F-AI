<script lang="ts">
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  let active = $state(false)

  function toggleActive() {
    active = !active
  }
</script>

<button
  class="btn btn-sm"
  class:btn-active={active}
  class:text-blue={active}
  class:bg-gray-200={active}
  onclick={() => toggleActive()}
>
  <Icon icon={icons["globe"]} width={16} height={16} />
  Search
</button>

<style>
  .text-blue {
    color: #3b82f6;
  }

  .text-blue :global(svg) {
    stroke: currentColor;
  }
</style>
