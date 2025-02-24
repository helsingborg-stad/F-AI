<script lang="ts">
	import { icons } from '$lib/components/Icon/icons.js';
	import Icon from '$lib/components/Icon/Icon.svelte';

	export let iconName: keyof typeof icons;
	export let title: string;
	export let onClick: () => void;
</script>

<button
	class="flex gap-2 items-center px-4 py-1.5 text-sm cursor-pointer hover:bg-gray-100 rounded-md"
	on:click={onClick}
>
	{#if iconName && icons[iconName]}
		<Icon icon={icons[iconName]} width={16} height={16}/>
	{/if}
	{title}
</button>