<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'

  interface Props {
    items: IMenuItem[],
    activePath: string
  }

  const { items, activePath }: Props = $props()

  function isActive(path: string) {
    return activePath.endsWith(path)
  }
</script>

<ul class="menu">
  {#each items as item}
    <li>
      <a href={item.path} class:active={isActive(item.path)}>{item.label}</a>
    </li>
  {/each}
</ul>