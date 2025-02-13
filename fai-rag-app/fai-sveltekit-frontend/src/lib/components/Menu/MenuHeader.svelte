<script lang="ts">
	import Icon from '$lib/components/Icon/Icon.svelte';
	import { icons } from '$lib/components/Icon/icons.js';

	export let title: string = '';
	export let iconName: keyof typeof Icon;
</script>

<button class="btn">
	{#if iconName && icons[iconName]}
		<Icon icon={ icons[iconName] } />
	{/if}
	{title}
</button>