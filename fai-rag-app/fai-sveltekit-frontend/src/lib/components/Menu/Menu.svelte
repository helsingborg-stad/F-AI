<script lang="ts">
	import type { MenuItem } from '$lib/types.js';

	export let items: MenuItem[] = [];
	export let currentUrlPath: string;

	$: urlFirstDirectory = (() => {
		const segments = currentUrlPath.split('/').filter(Boolean);
		return segments.length > 0 ? '/' + segments[0] : '/';
	})();

	const isActive = (path: string) => path === urlFirstDirectory;
</script>

<div class="h-full">
	<ul class="menu">
		{#each items as item}
			<li>
				<a href="{item.path}" class:active={isActive(item.path)}>{item.label}</a>
			</li>
		{/each}
	</ul>
</div>