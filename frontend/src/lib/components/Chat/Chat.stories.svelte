<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Chat from '$lib/components/Chat/Chat.svelte'
  import { fn } from '@storybook/test'
  import dayjs from 'dayjs'

  const { Story } = defineMeta({
    title: 'Components/Chat/Chat',
    component: Chat,
    tags: ['autodocs'],
  })
</script>

<Story
  name="default"
  args={{
    messages: [
      {
        timestamp: dayjs().subtract(30, 'seconds').toISOString(),
        source: 'user',
        message: 'Hello world!',
      },
      {
        timestamp: dayjs().subtract(15, 'seconds').toISOString(),
        source: 'assistant',
        message:
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, metus eu tincidunt tincidunt, metus odio tincidunt sapien, sed congue metus sapien eu metus.',
      },
      { timestamp: dayjs().toISOString(), source: 'user', message: 'Agree' },
    ],
    inputPlaceholder: 'Fråga Folkets AI',
    onSubmitMessage: fn(),
  }}
/>
