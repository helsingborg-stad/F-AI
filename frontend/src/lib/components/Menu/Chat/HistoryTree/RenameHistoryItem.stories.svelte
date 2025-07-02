<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import RenameConversationModal from '$lib/components/Menu/Chat/RenameConversationModal.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/RenameConversationModal',
    tags: ['autodocs'],
  })

  let defaultComponentRef: RenameConversationModal

  function handleSave(conversationId: string, newTitle: string) {
    console.log(`Saved chat ID "${conversationId}" with new title "${newTitle}"`)
  }
</script>

<Story name="Default">
  <RenameConversationModal
    bind:this={defaultComponentRef}
    onSave={handleSave}
  />
  <button
    class="btn btn-primary mt-4"
    onclick={() => defaultComponentRef?.showModal('chat-123', 'Current Chat Title')}
  >
    Open Rename Dialog
  </button>
</Story>
