<script module lang="ts">
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import { action } from '@storybook/addon-actions'
	import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte';

	const { Story } = defineMeta({
		title: 'Components/Menu/Chat/History',
		component: HistoryItem,
		tags: ['autodocs'],
		argTypes: {
			title: { control: 'text' },
			itemOptions: {
				control: 'object',
				description: 'Array of menu options'
			}
		}
	})
</script>

<Story name="Default" args={{ title: "Chat conversation with no options" }} />

<Story name="With options" args={{
	title: "Chat conversation with options",
	itemOptions: [
		{
			iconName: "pencil",
			title: "Rename",
			onClick: (evt: Event) => {
				action('clicked')(evt);
			}
		},
		{
			iconName: "trash",
			title: "Delete",
			onClick: (evt: Event) => {
				action('clicked')(evt);
			}
		}
	]}} />
