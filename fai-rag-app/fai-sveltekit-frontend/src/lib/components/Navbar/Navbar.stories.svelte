<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import Navbar from '$lib/components/Navbar/Navbar.svelte';

	const { Story } = defineMeta({
		title: 'Components/Navbar',
		component: Navbar,
		tags: ['autodocs'],
	});
</script>

<Story name="Menu button for `md` view ports" />