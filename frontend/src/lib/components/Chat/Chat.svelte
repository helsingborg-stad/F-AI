<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import ChatMessage from '$lib/components/Chat/ChatMessage.svelte'
  import ChatInput from '$lib/components/Chat/ChatInput.svelte'
  import ActionButtons, {
    type AllowedFeature,
  } from '$lib/components/Chat/ChatInput/ActionButtons.svelte'
  import type { IAssistantMenu } from '$lib/types.js'

  interface Message {
    timestamp: string
    source: string
    message: string
    reasoning: string
    showLoader: boolean
  }

  export interface Props {
    assistants: IAssistantMenu[]
    selectedAssistantId: string
    messages: Message[]
    inputPlaceholder: string
    onSubmitMessage: (message: string) => void
    chatStateIdle: boolean
    onStopChat: () => void
    enabledFeatures: string[]
  }

  let {
    assistants,
    selectedAssistantId = $bindable(),
    messages,
    inputPlaceholder,
    onSubmitMessage,
    chatStateIdle,
    onStopChat,
    enabledFeatures = $bindable(),
  }: Props = $props()

  let scrollContainer: HTMLDivElement = undefined as unknown as HTMLDivElement

  let isContentNearBottom = $state(false)
  let chatInput = $state('')
  const disableAssistantPicker = $derived(messages && messages.length > 0)

  const contentIsScrollable = $derived(
    messages.length > 0 &&
      scrollContainer &&
      scrollContainer.scrollHeight > scrollContainer.clientHeight,
  )

  function scrollToBottom() {
    scrollContainer.scroll({ top: scrollContainer.scrollHeight, behavior: 'smooth' })
  }

  function onScroll() {
    const margin = 50
    isContentNearBottom =
      scrollContainer &&
      scrollContainer.scrollHeight -
        scrollContainer.scrollTop -
        scrollContainer.clientHeight <=
        margin
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

  const selectedAssistant = $derived(
    selectedAssistantId
      ? assistants.flatMap((g) => g.menuItems).find((i) => i.id === selectedAssistantId)
      : undefined,
  )

  let allowedFeatures: AllowedFeature[] = $derived(
    selectedAssistant
      ? [
          selectedAssistant.allowSearch === true && {
            id: 'web_search',
            title: 'Web search',
            icon: icons['globe'],
          },
          selectedAssistant.allowReasoning === true && {
            id: 'reasoning',
            title: 'Reasoning',
            icon: icons['brain'],
          },
          selectedAssistant.allowImageGeneration === true && {
            id: 'image_gen',
            title: 'Image generation',
            icon: icons['image'],
          },
        ].filter<AllowedFeature>((v) => v !== false)
      : [],
  )
</script>

<div class="flex h-full flex-col">
  <!-- Chat Bubbles Area -->
  <div bind:this={scrollContainer} onscroll={onScroll} class="flex-1 overflow-auto p-4">
    {#each messages as msg, i (`${i}${msg.source}`)}
      <ChatMessage
        sender={msg.source}
        details={msg.reasoning}
        text={msg.message}
        time={msg.timestamp}
        showLoader={msg.showLoader}
      />
    {/each}
  </div>

  <!-- Chat Input -->
  <div class="relative flex-shrink-0 px-3 pb-3 md:px-6 md:pb-6">
    <div
      class="absolute inset-x-0 bottom-20 flex justify-center transition md:bottom-40"
      class:translate-y-12={isContentNearBottom}
      class:md:translate-y-24={isContentNearBottom}
      class:invisible={!contentIsScrollable}
    >
      <button
        onclick={scrollToBottom}
        class="rounded-full bg-white p-2 shadow transition hover:bg-gray-100 active:scale-95"
      >
        <Icon icon={icons.scroll} />
      </button>
    </div>
    <div class="relative z-10 mx-auto w-full max-w-[60rem] rounded-2xl border bg-white">
      <ChatInput
        placeholder={inputPlaceholder}
        bind:value={chatInput}
        onSubmit={onHandleSubmit}
        disabled={selectedAssistantId === ''}
        receivingMessage={!chatStateIdle}
        {onStopChat}
      >
        <ActionButtons
          {allowedFeatures}
          bind:enabledFeatureIds={enabledFeatures}
          {assistants}
          bind:selectedAssistantId
          {disableAssistantPicker}
        />
      </ChatInput>
    </div>
  </div>
</div>
