<script lang="ts">
	import type { MenuItem } from '$lib/types.js';
	import Menu from '$lib/components/Menu/Menu.svelte';

	export let menuSidebarItems: MenuItem[] = [];
	export let currentUrlPath: string = '/';
</script>

<nav>
	<Menu items={menuSidebarItems} {currentUrlPath} />
</nav>
