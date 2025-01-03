<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import Navbar from '$lib/components/Navbar/Navbar.svelte';

	const { Story } = defineMeta({
		title: 'Components/Navbar',
		component: Navbar,
		tags: ['autodocs'],
		argTypes: {
			title: { control: 'text' },
		},
	});
</script>

<!-- Navbar hidden for larger screens. -->
<Story name="Hidden for `md` view ports" />