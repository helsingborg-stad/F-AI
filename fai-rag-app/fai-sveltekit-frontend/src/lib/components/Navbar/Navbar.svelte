<!--TODO: Remove dropdown from navbar and place it in top `+layout.page`-->
<script lang="ts">
	import type { MenuItem } from '$lib/types.js';

	export let navbarTitle: string = '';

	export let avatarUrl: URL | null = null;
	export let avatarName: string = '';

	export let navBarItems: MenuItem[] = [];
	export let currentUrlPath: string;

	$: urlFirstDirectory = (() => {
		const segments = currentUrlPath.split('/').filter(Boolean);
		return segments.length > 0 ? `/${segments[0]}` : '/';
	})();

	const isActive = (path: string) => path === urlFirstDirectory;
</script>

<nav class="navbar">
	<div class="md:grow-0 grow">
		<div class="dropdown">
			<div tabindex="0" role="button" class="btn btn-ghost btn-circle md:hidden">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 6h16M4 12h16M4 18h7" />
				</svg>
			</div>
			<ul class="menu dropdown-content bg-base-200 z-10 mt-3 w-52 p-2 shadow gap-3">
				{#each navBarItems as { label, path }}
					<li><a href="{path}" class:active={isActive(path)}>{label}</a></li>
				{/each}
			</ul>
		</div>
		<div class="grow">
			{#if navbarTitle}
				<span>{navbarTitle}</span>
			{/if}
		</div>
	</div>
	<div class="hidden md:flex justify-end grow">
		<ul class="menu menu-horizontal gap-2">
			{#each navBarItems as { label, path }}
				<li><a href="{path}" class:active={isActive(path)}>{label}</a></li>
			{/each}
		</ul>
	</div>
	<div class="flex-none">
		{#if avatarUrl}
			<div class="btn btn-ghost btn-circle avatar">
				<div class="w-10 rounded-full">
					<img src="{avatarUrl.toString()}" alt="{avatarName}">
				</div>
			</div>
		{/if}
	</div>
</nav>
