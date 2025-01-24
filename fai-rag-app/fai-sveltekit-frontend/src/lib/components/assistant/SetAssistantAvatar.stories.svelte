<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import SetAssistantAvatar from './SetAssistantAvatar.svelte';

	const { Story } = defineMeta({
		title: 'Components/Set Assistant Avatar',
		component: SetAssistantAvatar,
		tags: ['autodocs'],
		argTypes: {
			avatarSrc: {
				control: 'text',
				description: 'Source URL of the avatar image.',
			},
		},
	})
</script>

<Story
	name="Default"
	args={{
		avatarSrc: '',
	}}
>
	<SetAssistantAvatar />
</Story>