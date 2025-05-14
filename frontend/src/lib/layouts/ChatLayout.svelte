<script lang="ts">
  import { page } from '$app/state'
  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte'
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'

  type Props = ChatProps & {
    assistants: {
      id: string,
      name: string
    }[]
    selectedAssistantId: string
    conversationId: string
  }

  let {
    messages,
    assistants,
    inputPlaceholder,
    onSubmitMessage,
    selectedAssistantId = $bindable(),
    conversationId
  }: Props = $props()
</script>

<div class="flex bg-base-200 max-h-full flex-grow overflow-hidden">
  <aside class="w-60 flex-shrink-0 overflow-hidden bg-base-200 bg-[rgba(255,255,0,0.5)] max-md:!w-0">
    <MenuSidebar
      menuSidebarTitle="Chat"
      menuSidebarItems={[]}
      currentUrlPath={page.url.pathname}
    />
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