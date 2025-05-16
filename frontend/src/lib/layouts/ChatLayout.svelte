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
  }

  let {
    messages,
    assistants,
    conversations,
    inputPlaceholder,
    onSubmitMessage,
    selectedAssistantId = $bindable(),
    conversationId,
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
          options: [],
          createdTimestamp: c.timestamp
        }))}
          highlightedIds={[conversationId]}
          onClick={(id) => goto(`/chat/${id}`)}
        />
      </div>
    </SidebarMenu>
  </aside>
  <div class="flex flex-col gap-2 p-2 grow ">
    <div class="flex items-center gap-2">
      <select
        class="select select-bordered select-sm text-sm"
        bind:value={selectedAssistantId}
      >
        <option value="" disabled selected>Select assistant</option>
        {#each assistants as assistant(assistant.id)}
          <option value={assistant.id}>{assistant.name}</option>
        {/each}
      </select>
      <span class="label-text-alt opacity-50">{conversationId}</span>
    </div>
    <main class="grow rounded-lg border bg-stone-50 overflow-auto">
      <Chat
        messages={messages}
        inputPlaceholder={inputPlaceholder}
        {onSubmitMessage}
      />
    </main>
  </div>
</div>