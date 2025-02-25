<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import HistoryItemOptions from '$lib/components/Menu/Chat/HistoryItemOptions.svelte';


	const { Story } = defineMeta({
		title: 'Components/Menu/Chat/History/Options',
		component: HistoryItemOptions,
		tags: ['autodocs'],
		argTypes: {
			iconName: {
				control: 'text',
			},
			title: { control: 'text' },
			onClick: { action: 'clicked' }
		}
	});
</script>

<Story name="Default" args={{ iconName: "trash", title: "Delete" }} />