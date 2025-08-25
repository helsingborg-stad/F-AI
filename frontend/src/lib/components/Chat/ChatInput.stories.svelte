<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ChatInput from './ChatInput.svelte'
  import ActionButtons from '$lib/components/Chat/ChatInput/ActionButtons.svelte'
  import { mockOnlyAssistants } from '$stories/assets/mockData/assistantPicker.ts'

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatInput',
    tags: ['autodocs'],
  })
</script>

<Story name="Default">
  <ChatInput
    placeholder=""
    value=""
    onSubmit={() => {
      console.log('Send message!')
    }}
  >
    <div></div>
  </ChatInput>
</Story>

<Story name="With action button model picker">
  <ChatInput
    placeholder=""
    value=""
    onSubmit={() => {
      console.log('Send message!')
    }}
  >
    <ActionButtons
      assistants={mockOnlyAssistants}
      selectedAssistantId={mockOnlyAssistants[0].menuItems[0].id}
      disableAssistantPicker={false}
    />
  </ChatInput>
</Story>
