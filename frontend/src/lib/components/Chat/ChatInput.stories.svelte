<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatInput from './ChatInput.svelte'

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatInput',
    tags: ['autodocs'],
  })
</script>

<Story name="Default">
  <ChatInput placeholder='' value='' onSubmit={() => {console.log('Send message!')}}>
    <div></div>
  </ChatInput>
</Story>