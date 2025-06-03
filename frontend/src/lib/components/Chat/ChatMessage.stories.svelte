<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatMessage from '$lib/components/Chat/ChatMessage.svelte'

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatMessage',
    component: ChatMessage,
    tags: ['autodocs'],
    argTypes: {
      sender: {
        control: { type: 'radio' },
        options: ['user', 'bot'],
        description: 'Determines the alignment and message styling.',
      },
      text: { control: 'text', description: 'The message text' },
      time: { control: 'text', description: 'Timestamp of the message.' },
    },
  })
</script>

<Story
  name="Default"
  args={{
    sender: 'user',
    text: 'Hello, this is a message!',
    time: '2025-05-15 15:16:13',
  }}
/>

<Story
  name="Bot message"
  args={{
    sender: 'bot',
    text: 'Hello, this is a bot message!',
  }}
/>
