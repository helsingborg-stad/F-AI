<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatBubble from '$lib/components/Chat/ChatBubble.svelte'

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatBubble',
    component: ChatBubble,
    tags: ['autodocs'],
    argTypes: {
      sender: {
        control: { type: 'radio' },
        options: ['user', 'bot'],
        description: 'Determines the alignment of the chat bubble.',
      },
      text: { control: 'text', description: 'The message text.' },
      name: { control: 'text', description: 'Name of the sender.' },
      time: { control: 'text', description: 'Timestamp of the message.' },
      avatar: { control: 'text', description: "URL of the sender's avatar image." },
      status: { control: 'text', description: 'Status text (e.g., "Delivered").' },
      bubbleColor: {
        control: { type: 'select' },
        options: [
          '',
          'primary',
          'secondary',
          'accent',
          'info',
          'success',
          'warning',
          'error',
        ],
        description: 'Color of the chat bubble.',
      },
    },
  })
</script>

<Story
  name="User Message"
  args={{
    sender: 'user',
    text: 'Hello, this is a user message!',
    name: 'User',
    time: '12:00',
    avatar: 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
    status: 'Seen',
    bubbleColor: 'primary',
  }}
/>

<Story
  name="Bot Message"
  args={{
    sender: 'bot',
    text: 'Hello, this is a bot response!',
    name: 'Bot',
    time: '12:01',
    avatar: 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
    status: 'Delivered',
    bubbleColor: 'secondary',
  }}
/>

<Story
  name="Message Without Avatar"
  args={{
    sender: 'bot',
    text: 'This message has no avatar.',
    name: 'System',
    time: '12:02',
    status: 'Delivered',
    bubbleColor: 'accent',
  }}
/>

<Story
  name="Simple Message"
  args={{
    sender: 'user',
    text: 'Just a simple message without additional info.',
  }}
/>
