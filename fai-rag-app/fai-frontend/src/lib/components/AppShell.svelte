<script lang="ts">
  import { path, searchParams, url } from 'elegua'
  export let hasDrawer: boolean | null = null

  let drawerIsOpen = false

  const closeOnChange = (_: any) => false

  $: drawerIsOpen = closeOnChange($url)
</script>

<div
  class:drawer={$$slots?.drawer || hasDrawer}
  class:lg:drawer-open={$$slots?.drawer || hasDrawer}
  {...$$props}
>
  {#if $$slots?.drawer || hasDrawer}
    <input
      id="my-drawer-2"
      type="checkbox"
      class="drawer-toggle"
      checked={drawerIsOpen}
      on:change={() => (drawerIsOpen = !drawerIsOpen)}
    />
    <slot name="drawer" />
  {/if}

  <slot />
</div>
