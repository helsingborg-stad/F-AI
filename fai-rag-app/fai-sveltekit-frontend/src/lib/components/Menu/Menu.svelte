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

<ul class="menu">
	{#each items as { path, label }}
		<li class="py-1">
			<a href="{path}" class:active={isActive(path)}>{label}</a>
		</li>
	{/each}
</ul>
