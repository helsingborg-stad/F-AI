<script lang="ts">
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree/HistoryTree.svelte'
  import { goto } from '$app/navigation'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import RenameConversationModal from '$lib/components/Menu/Chat/RenameConversationModal.svelte'
  import { uiState } from '$lib/state/ui.svelte.js'

  type Props = ChatProps & {
    canChat: boolean
    assistants: IAssistantMenu[]
    conversations: {
      id: string,
      timestamp: string,
      title: string
    }[]
    selectedAssistantId: string
    conversationId: string
    onRenameConversation: (id: string, title: string) => void
    onDeleteConversation: (id: string) => void
    onStartNewChat: () => void
    chatStateIdle: boolean
    onStopChat: () => void
    enableSearch: boolean
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
    onRenameConversation,
    onDeleteConversation,
    onStartNewChat,
    chatStateIdle,
    onStopChat,
    enableSearch = $bindable(),
  }: Props = $props()

  let renameModal: RenameConversationModal

  function openRenameModal(id: string, title: string) {
    if (renameModal) renameModal.showModal(id, title)
  }

  $effect(() => {
    let resizeTimer: number

    const handleResize = () => {
      clearTimeout(resizeTimer)
      resizeTimer = setTimeout(() => {
        const isMobile = window.innerWidth < 768
        uiState.showSidebar = !isMobile
      }, 500)
    }

    handleResize()
    window.addEventListener('resize', handleResize)

    return () => {
      clearTimeout(resizeTimer)
      window.removeEventListener('resize', handleResize)
    }
  })
</script>

<div class="flex bg-base-200 h-full overflow-hidden relative">
  {#if uiState.showSidebar}
    <button
      type="button"
      aria-label="Close sidebar"
      class="fixed inset-0 z-[999] bg-transparent cursor-default p-0 border-0 md:hidden"
      onclick={() => uiState.showSidebar = false}
    ></button>
  {/if}

  <aside
    class="w-60 flex-shrink-0 bg-base-200 max-md:absolute max-md:top-0 max-md:left-0 max-md:h-full max-md:z-[1000] max-md:shadow-[2px_0_8px_rgba(0,0,0,0.15)] max-md:backdrop-blur"
    class:hidden={!uiState.showSidebar}
  >
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
            { iconName: 'pencil', title: 'Edit', onClick: () => openRenameModal(c.id, c.title) },
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
  <div class="flex flex-col w-full h-full gap-2 p-2 pt-0 overflow-hidden">
    <main class="flex-grow h-full rounded-lg border bg-stone-50 overflow-hidden">
      <Chat
        {assistants}
        bind:selectedAssistantId
        messages={messages}
        inputPlaceholder={inputPlaceholder}
        {onSubmitMessage}
        {chatStateIdle}
        {onStopChat}
        bind:enableSearch
      />
    </main>
  </div>
</div>

<RenameConversationModal
  onSave={onRenameConversation}
  bind:this={renameModal}
/>