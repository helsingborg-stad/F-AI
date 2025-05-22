<script lang="ts">
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree/HistoryTree.svelte'
  import { goto } from '$app/navigation'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  type Props = ChatProps & {
    canChat: boolean
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
    onStartNewChat: () => void
  }

  let {
    canChat,
    messages,
    assistants,
    conversations,
    inputPlaceholder,
    onSubmitMessage,
    selectedAssistantId = $bindable(),
    conversationId,
    onDeleteConversation,
    onStartNewChat,
  }: Props = $props()
</script>

<div class="flex flex-col md:flex-row bg-base-200 h-full overflow-hidden">
  <aside class="hidden md:block md:w-60 flex-shrink-0 bg-base-200">
    <SidebarMenu title="Chat">
      <div class="flex flex-col h-full gap-2">
        <button type="button" class="btn btn-neutral btn-sm" disabled={!canChat} onclick={onStartNewChat}>
          <Icon icon={icons["plus"]} width={16} height={16} />
          <span class="text-s">Start New Chat</span>
        </button>
        <div class="pl-2 overflow-y-auto h-full">
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
      </div>
    </SidebarMenu>
  </aside>
  <div class="flex flex-col w-full gap-2 p-2 pt-0 overflow-hidden">
    <main class="flex-grow rounded-lg border bg-stone-50 overflow-auto">
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