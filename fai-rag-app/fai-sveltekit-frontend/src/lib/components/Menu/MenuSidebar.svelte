<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import Menu from '$lib/components/Menu/Menu.svelte'

  export let menuSidebarItems: IMenuItem[] = []
  export let currentUrlPath: string = '/'
</script>

<nav>
  <Menu items={menuSidebarItems} {currentUrlPath} />
</nav>
