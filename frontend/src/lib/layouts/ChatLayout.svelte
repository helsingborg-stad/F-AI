<script lang="ts">
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree/HistoryTree.svelte'
  import { goto } from '$app/navigation'

  type Props = ChatProps & {
    assistants: {
      id: string,
      name: string
    }[]
    conversations: {
      id: string,
      timestamp: string,
      title: string
    }[]
    selectedAssistantId: string
    conversationId: string
    onDeleteConversation: (id: string) => void
  }

  let {
    messages,
    assistants,
    conversations,
    inputPlaceholder,
    onSubmitMessage,
    selectedAssistantId = $bindable(),
    conversationId,
    onDeleteConversation
  }: Props = $props()
</script>

<div class="flex bg-base-200 max-h-full flex-grow overflow-hidden">
  <aside class="w-60 flex-shrink-0 bg-base-200 max-md:!w-0">
    <SidebarMenu title="Chat">
      <div class="pl-2">
        <HistoryTree
          items={conversations.map(c => ({
          id: c.id,
          title: c.title || c.id,
          options: [
            { iconName: 'trash', title: 'Delete', onClick: () => onDeleteConversation(c.id) },
          ],
          createdTimestamp: c.timestamp
        }))}
          highlightedIds={[conversationId]}
          onClick={(id) => goto(`/chat/${id}`)}
        />
      </div>
    </SidebarMenu>
  </aside>
  <div class="flex flex-col gap-2 p-2 grow ">
    <main class="grow rounded-lg border bg-stone-50 overflow-auto">
      <Chat
        {assistants}
        bind:selectedAssistantId
        messages={messages}
        inputPlaceholder={inputPlaceholder}
        {onSubmitMessage}
      />
    </main>
  </div>
</div>