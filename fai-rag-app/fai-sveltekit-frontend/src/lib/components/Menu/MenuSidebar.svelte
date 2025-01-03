<script lang="ts">
	import type { MenuItem } from '$lib/types.js';
	import Menu from '$lib/components/Menu/Menu.svelte'

	export let menuItems: MenuItem[] = [];
	export let currentUrlPath: string = '/';
</script>

<div class="flex-shrink-0 overflow-x-hidden bg-gray-50 max-md:!w-0 z-[1] w-60">
	<div class="h-full">
		<Menu items={menuItems} currentUrlPath={currentUrlPath}/>
	</div>
</div>
