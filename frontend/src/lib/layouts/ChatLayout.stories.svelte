<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import dayjs from 'dayjs'

  const { Story } = defineMeta({
    title: 'Layouts/Chat',
    component: ChatLayout,
    tags: ['autodocs'],
  })
</script>

<script>
  import { action } from '@storybook/addon-actions'
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
    assistants: [
      { id: 'ai1', name: 'Folkets AI' },
      { id: 'ai2', name: 'Support AI' },
    ],
    conversations: [
      {
        id: 'conv1',
        timestamp: dayjs().subtract(2, 'days').toISOString(),
        title: 'Previous conversation',
      },
      {
        id: 'conv2',
        timestamp: dayjs().subtract(1, 'day').toISOString(),
        title: 'Recent chat',
      },
      { id: 'current', timestamp: dayjs().toISOString(), title: 'Current conversation' },
    ],
    selectedAssistantId: 'ai1',
    conversationId: 'current',
    inputPlaceholder: 'Fråga Folkets AI',
    onSubmitMessage: action('onSubmitMessage'),
    onStartNewChat: action('onStartNewChat'),
    onDeleteConversation: action('onDeleteConversation'),
    canChat: true,
  }}
/>
