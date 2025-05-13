<script lang="ts">
  import ChatBubble from '$lib/components/Chat/ChatBubble.svelte'
  import ChatInput from '$lib/components/Chat/ChatInput.svelte'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

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

  $effect(() => {
    if (messages && messages.length > 0 && isContentNearBottom) {
      scrollToBottom()
    }
  })

  function getBubbleColor(source: string) {
    switch (source) {
      case 'error':
        return 'error'
      case 'user':
        return 'primary'
      default:
        return 'secondary'
    }
  }
</script>

<div class="flex flex-col h-full max-h-full">
  <!-- Chat Bubbles Area -->
  <div
    bind:this={scrollContainer}
    onscroll={onScroll}
    class="overflow-auto grow p-4"
  >
    {#each messages as msg (`${msg.timestamp}${msg.message}`)}
      <ChatBubble sender={msg.source} name={msg.source} text={msg.message} time={msg.timestamp}
                  bubbleColor={getBubbleColor(msg.source)} />
    {/each}
  </div>

  <!-- Chat Input -->
  <div class="relative p-6">
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
    <div class="relative rounded-2xl border bg-white p-2 z-10">
      <ChatInput send={onSubmitMessage} placeholder={inputPlaceholder} />
    </div>
  </div>
</div>