<script lang="ts">
  import type { IMenuItem } from '$lib/types.js'
  import Menu from '$lib/components/Menu/Menu.svelte'

  export let menuSidebarTitle: string = ''
  export let menuSidebarItems: IMenuItem[] = []
  export let currentUrlPath: string = '/'
</script>

<nav>
  <Menu title={menuSidebarTitle} items={menuSidebarItems} {currentUrlPath} />
</nav>
