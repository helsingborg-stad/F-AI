<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatInput from './ChatInput.svelte'
  import ActionButtons from '$lib/components/Chat/ChatInput/ActionButtons.svelte'

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatInput',
    tags: ['autodocs'],
  })

  const assistants = [
    { id: '0', name: 'Language assistant' },
    { id: '1', name: 'Math assistant' },
  ]
</script>

<Story name="Default">
  <ChatInput placeholder='' value='' onSubmit={() => {console.log('Send message!')}}>
    <div></div>
  </ChatInput>
</Story>

<Story name="With action button model picker">
  <ChatInput placeholder='' value='' onSubmit={() => {console.log('Send message!')}}>
    <ActionButtons {assistants} selectedAssistantId={assistants[0].id} />
  </ChatInput>
</Story>