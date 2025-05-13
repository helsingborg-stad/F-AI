<script lang="ts">
  import { page } from '$app/state'
  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte'
  import Chat from '$lib/components/Chat/Chat.svelte'
  import type { Props as ChatProps } from '$lib/components/Chat/Chat.svelte'

  type Props = ChatProps

  const { messages, inputPlaceholder, onSubmitMessage }: Props = $props()
</script>

<div class="flex bg-base-200 max-h-full flex-grow overflow-hidden">
  <aside class="w-60 flex-shrink-0 bg-base-200 max-md:!w-0">
    <MenuSidebar
      menuSidebarTitle="Chat"
      menuSidebarItems={[]}
      currentUrlPath={page.url.pathname}
    />
  </aside>
  <main class="m-2 w-full rounded-lg border bg-stone-50 overflow-auto">
    <Chat messages={messages} inputPlaceholder={inputPlaceholder} onSubmitMessage={onSubmitMessage} />
  </main>
</div>