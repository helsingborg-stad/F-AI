<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import Menu from '$lib/components/Menu/Menu.svelte';

	const { Story } = defineMeta({
		title: 'Components/Menu/Menu',
		component: Menu,
		tags: ['autodocs'],
		argTypes: {
			title: { control: 'object' },
		},
	});

	// Sample menu items
	const sampleItems = [
		{ label: 'Home', path: '/' },
		{ label: 'About', path: '/about' },
		{ label: 'Contact', path: '/contact' },
	];
</script>

<Story name="Default" args={{ items: sampleItems, currentUrlPath: '/' }} />