<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import MenuHeader from '$lib/components/Menu/MenuHeader.svelte'

  export let items: IMenuItem[] = []
  export let currentUrlPath: string

  $: urlFirstDirectory = (() => {
    const segments = currentUrlPath.split('/').filter(Boolean)
    return segments.length > 0 ? '/' + segments[0] : '/'
  })()

  const isActive = (path: string) => path === urlFirstDirectory
</script>

<div class="h-full">
  <MenuHeader iconName="banana" title="Banana menu" />
  <ul class="menu">
    {#each items as item}
      <li>
        <a href={item.path} class:active={isActive(item.path)}>{item.label}</a>
      </li>
    {/each}
  </ul>
</div>
