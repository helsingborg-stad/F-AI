<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree/HistoryTree.svelte'
  import { goto } from '$app/navigation'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import RenameConversationModal from '$lib/components/Menu/Chat/RenameConversationModal.svelte'
  import ResponsiveSidebar from '$lib/components/Menu/Chat/ResponsiveSidebar.svelte'
  import type { FileWithState } from '$lib/files/useInlineFiles.js'

  type Props = ChatProps & {
    canChat: boolean
    assistants: IAssistantMenu[]
    conversations: {
      id: string
      timestamp: string
      title: string
    }[]
    selectedAssistantId: string
    conversationId: string
    onRenameConversation: (id: string, title: string) => void
    onDeleteConversation: (id: string) => void
    onStartNewChat: () => void
    chatStateIdle: boolean
    onStopChat: () => void
    enabledFeatures: string[]
    inlineFiles: FileWithState[]
    onFilesChanged: (files: File[]) => void
    canChangeFiles: boolean
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
    enabledFeatures = $bindable(),
    inlineFiles,
    onFilesChanged,
    canChangeFiles,
  }: Props = $props()

  let renameModal: RenameConversationModal

  function openRenameModal(id: string, title: string) {
    if (renameModal) renameModal.showModal(id, title)
  }
</script>

<div class="relative flex h-full overflow-hidden bg-base-200">
  <ResponsiveSidebar>
    <SidebarMenu>
      <div class="flex h-full flex-col gap-2">
        <button
          type="button"
          class="btn btn-neutral btn-sm"
          disabled={!canChat}
          onclick={onStartNewChat}
        >
          <Icon icon={icons['plus']} width={16} height={16} />
          <span class="text-s">{m.chat_action_start_new()}</span>
        </button>
        <div class="h-full overflow-y-auto pl-2">
          <HistoryTree
            items={conversations.map((c) => ({
              id: c.id,
              title: c.title || c.id,
              options: [
                {
                  iconName: 'trash',
                  title: m.chat_history_action_delete(),
                  onClick: () => onDeleteConversation(c.id),
                },
                {
                  iconName: 'pencil',
                  title: m.chat_history_action_edit(),
                  onClick: () => openRenameModal(c.id, c.title),
                },
              ],
              createdTimestamp: c.timestamp,
            }))}
            highlightedIds={[conversationId]}
            onClick={(id) => goto(`/chat/${id}`)}
          />
        </div>
      </div>
    </SidebarMenu>
  </ResponsiveSidebar>
  <div class="flex h-full w-full flex-col gap-2 overflow-hidden p-2 pt-0">
    <main class="h-full flex-grow overflow-hidden rounded-lg border bg-stone-50">
      <Chat
        {assistants}
        bind:selectedAssistantId
        {messages}
        {inputPlaceholder}
        {onSubmitMessage}
        {chatStateIdle}
        {onStopChat}
        bind:enabledFeatures
        {onFilesChanged}
        {inlineFiles}
        {canChangeFiles}
      />
    </main>
  </div>
</div>

<RenameConversationModal onSave={onRenameConversation} bind:this={renameModal} />
