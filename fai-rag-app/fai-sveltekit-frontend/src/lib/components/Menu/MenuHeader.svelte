<script lang="ts">
	import Icon from '$lib/components/Icon/Icon.svelte';
	import { icons } from '$lib/components/Icon/icons.js';

	export let title: string = '';
	export let iconName: keyof typeof icons;
	export let href: string = '#';
</script>

<ul class="menu">
	<li>
    <a href={href}>
			{#if iconName && icons[iconName]}
				<Icon icon={ icons[iconName] } />
			{/if}
			<p class="uppercase">{title}</p>
    </a>
  </li>
</ul>