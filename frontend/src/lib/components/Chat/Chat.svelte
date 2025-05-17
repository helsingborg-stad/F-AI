<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import ChatMessage from '$lib/components/Chat/ChatMessage.svelte'
  import ChatInput from '$lib/components/Chat/ChatInput.svelte'

  interface Message {
    timestamp: string
    source: string
    message: string
  }

  export interface Props {
    messages: Message[],
    inputPlaceholder: string,
    onSubmitMessage: (message: string) => void
  }

  const { messages, inputPlaceholder, onSubmitMessage }: Props = $props()

  let scrollContainer: HTMLDivElement = undefined as unknown as HTMLDivElement

  let isContentNearBottom = $state(false)
  let chatInput = $state('')

  const contentIsScrollable = $derived(messages.length > 0 && scrollContainer && scrollContainer.scrollHeight > scrollContainer.clientHeight)

  function scrollToBottom() {
    scrollContainer.scroll({ top: scrollContainer.scrollHeight, behavior: 'smooth' })
  }

  function onScroll() {
    const margin = 50
    isContentNearBottom =
      scrollContainer &&
      scrollContainer.scrollHeight - scrollContainer.scrollTop - scrollContainer.clientHeight <= margin
  }

  function onHandleSubmit() {
    if (chatInput.trim()) {
      onSubmitMessage(chatInput)
      chatInput = ''
    }
  }

  $effect(() => {
    if (messages && messages.length > 0 && isContentNearBottom) {
      scrollToBottom()
    }
  })
</script>

<div class="flex flex-col h-full max-h-full">
  <!-- Chat Bubbles Area -->
  <div
    bind:this={scrollContainer}
    onscroll={onScroll}
    class="overflow-auto grow p-4"
  >
    {#each messages as msg (`${msg.timestamp}${msg.message}`)}
      <ChatMessage sender={msg.source} text={msg.message} time={msg.timestamp} />
    {/each}
  </div>

  <!-- Chat Input -->
  <div class="relative px-6 pb-6">
    <div
      class="absolute inset-x-0 bottom-32 flex justify-center transition"
      class:translate-y-24={isContentNearBottom}
      class:invisible={!contentIsScrollable}
    >
      <button
        onclick={scrollToBottom}
        class="rounded-full bg-white p-2 shadow transition hover:bg-gray-100 active:scale-95"
      >
        <Icon icon={icons.scroll} />
      </button>
    </div>
    <div class="relative rounded-2xl border bg-white z-10 w-[60rem] mx-auto">
      <ChatInput placeholder={inputPlaceholder} bind:value={chatInput} onSubmit={onHandleSubmit}>
        <div></div>
      </ChatInput>
    </div>
  </div>
</div>