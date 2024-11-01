<script lang="ts">
  import Button from '../Button.svelte'
  import ChatBubble from '../ChatBubble.svelte'
  import SvelteMarkdownWrapper from '$lib/components/SvelteMarkdownWrapper.svelte'
  import SVG from '$lib/components/SVG.svelte'
  import { findLastIndex } from '../../../util/array'
  import TokenCounter from '$lib/components/chat/TokenCounter.svelte'
  import { type ChatMessage, type IncomingMessage, incomingMessageToChatMessage, SSE } from '$lib/components/chat/SSE'

  interface Assistant {
    id: string
    name: string
    project: string
    description: string
    sampleQuestions: string[]
    maxTokens: number
  }

  interface InitialState {
    chat_id: string
    max_tokens: number
    history: IncomingMessage[]
  }

  export let assistants: Assistant[] = []
  export let initialState: InitialState | undefined

  export let termOfService: string = `
---

### Terms of Service for Folkets AI
Welcome to our AI chat service. By using this service, you agree to the following terms:

**1. Avoid Sharing Personal Information**
* **Do not enter personal or sensitive data into the chat.** This includes, but is not limited to, social security numbers, addresses, financial information, or any other confidential details.

**2. Data Handling and Third Parties**
* Information entered into the chat may be stored and processed by third-party services.
* The chat uses various logging tools to improve the service and user experience.

**3. Limitation of Liability**
 * The service is provided "as is".

---
By continuing to use Folkets AI, you confirm that you have read, understood, and agree to these terms of service.
    `

  let selectedAssistantId: string
  let selectedAssistant: Assistant | null = null
  let activeConversationId: string | null = null
  $: selectedAssistant = assistants.find((a) => a.id === selectedAssistantId) || null
  $: {
    if (initialState) {
      activeConversationId = initialState.chat_id
      messages = initialState.history.map(incomingMessageToChatMessage)
    } else {
      messages = []
    }
  }

  /** SSE */
  let messages: ChatMessage[] = []
  let currentMessageInput: string = ''
  let isRequestRunning: boolean = false
  let lastMessageErrored: Boolean = false

  let sse = new SSE(
    onSSEError,
    onSSEConversationIdUpdate,
    onAddOrUpdateMessage,
    onSSEStatusChanged,
  )

  function onSSEError() {
    lastMessageErrored = true
  }

  function onSSEConversationIdUpdate(id: string) {
    activeConversationId = id
  }

  function onAddOrUpdateMessage(message: ChatMessage) {
    const existingIndex = messages.findIndex(m => m.id === message.id)
    if (existingIndex > -1) {
      messages.splice(existingIndex, 1, {
        ...messages[existingIndex],
        ...message,
      })
      messages = [...messages]
      return
    }
    messages = [...messages, message]
  }

  function onSSEStatusChanged(inIsRequestRunning: boolean) {
    isRequestRunning = inIsRequestRunning
  }

  function createSSE(question: string) {
    lastMessageErrored = false
    sse.create(question, activeConversationId, selectedAssistant?.project, selectedAssistant?.id)
    currentMessageInput = ''
  }

  function closeSSE() {
    sse.close()
  }

  /** Token Counting */
  let exceededTokenCount: false
  let tokenCounter: TokenCounter
  $: activeConversationId && tokenCounter?.queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)
  $: messages && activeConversationId && tokenCounter?.queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)
  $: selectedAssistantId && tokenCounter?.queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)

  /** Scrolling */
  let contentScrollDiv: Element
  let isContentAtBottom: Boolean = true
  $: contentScrollDiv &&
  messages &&
  messages.length > 0 &&
  isContentAtBottom &&
  scrollContentToBottom()
  $: lastMessageErrored && setTimeout(scrollContentToBottom, 100)

  function updateBottomCheck() {
    const margin = 50
    isContentAtBottom =
      contentScrollDiv &&
      contentScrollDiv.scrollHeight -
      contentScrollDiv.scrollTop -
      contentScrollDiv.clientHeight <=
      margin
  }

  const scrollToBottom = (node: Element) => {
    node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
  }

  function scrollContentToBottom() {
    scrollToBottom(contentScrollDiv)
  }

  /** Misc UI */
  function clearChat() {
    messages = []
    activeConversationId = null
    lastMessageErrored = false
  }

  function handleTextareaKeypress(event: KeyboardEvent) {
    if (event.key == 'Enter' && !event.shiftKey) {
      event.preventDefault()
      if (!exceededTokenCount) createSSE(currentMessageInput)
    }
  }

  function formatMessageForMarkdown(content: string): string {
    return content.replace(/\n/g, `\n\n  `)
  }

  function askSampleQuestion(question: string) {
    createSSE(question)
  }

  function retryLastMessage() {
    lastMessageErrored = false
    const lastUserMessageIndex = findLastIndex(messages, (m) => m.isSelf)
    const lastQuestion = messages[lastUserMessageIndex].content
    messages = messages.slice(0, lastUserMessageIndex)
    createSSE(lastQuestion)
  }

  function formButtonClick() {
    if (isRequestRunning) {
      closeSSE()
      return
    }

    createSSE(currentMessageInput)
  }

  $: formButtonIcon = isRequestRunning
    ? 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNpcmNsZS1zdG9wIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIvPjxyZWN0IHg9IjkiIHk9IjkiIHdpZHRoPSI2IiBoZWlnaHQ9IjYiIHJ4PSIxIi8+PC9zdmc+'
    : 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlbmQiPjxwYXRoIGQ9Im0yMiAyLTcgMjAtNC05LTktNFoiLz48cGF0aCBkPSJNMjIgMiAxMSAxMyIvPjwvc3ZnPg=='
</script>

<div
  class="absolute bottom-0 top-16 grid w-full overflow-hidden lg:w-[calc(100%-20rem)]"
  class:grid-rows-[6rem_1fr_7rem]={!initialState}
  class:grid-rows-[1fr_7rem]={initialState}
>
  <!-- Floating controls -->
  <div
    class="absolute inset-x-0 bottom-32 z-10 flex justify-center transition"
    class:translate-y-20={isContentAtBottom}
  >
    <button
      on:click={scrollContentToBottom}
      class="rounded-full bg-white p-2 shadow transition hover:bg-gray-100 active:scale-95"
    >
      <SVG
        width="24"
        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWFycm93LWJpZy1kb3duLWRhc2giPjxwYXRoIGQ9Ik0xNSA1SDkiLz48cGF0aCBkPSJNMTUgOXYzaDRsLTcgNy03LTdoNFY5eiIvPjwvc3ZnPg=="
      />
    </button>
  </div>

  <!-- Top controls -->
  {#if !initialState}
    <div class="flex flex-col items-center justify-center gap-1 p-4">
      <select
        class="select select-bordered w-full max-w-xs"
        bind:value={selectedAssistantId}
        on:change={clearChat}
      >
        <option disabled selected value="">Choose assistant</option>
        {#each assistants as assistant (`${assistant.project}/${assistant.id}`)}
          <option value={assistant.id}>{assistant.name}</option>
        {/each}
      </select>
      <p class="text-sm" class:invisible={!activeConversationId}>
        conversation id: {activeConversationId}
      </p>
    </div>
  {/if}

  <!-- Content -->
  <div
    class="flex justify-center overflow-y-scroll"
    bind:this={contentScrollDiv}
    on:scroll={updateBottomCheck}
  >
    <div class="h-fit w-full max-w-prose">
      {#each messages as message (message.id)}
        <ChatBubble
          content={message.isSelf
            ? message.content
            : formatMessageForMarkdown(message.content)}
          isSelf={message.isSelf}
          enableMarkdown={!message.isSelf}
        />
      {:else}
        <div class="prose">
          {#if selectedAssistant}
            <SvelteMarkdownWrapper source={selectedAssistant.description} />
            <div class="flex gap-2 max-w-full flex-wrap justify-center">
              {#each selectedAssistant.sampleQuestions as question}
                <button
                  class="btn btn-outline"
                  on:click={() => askSampleQuestion(question)}
                >
                  {question}
                </button>
              {/each}
            </div>
          {:else}
            <p>
              Here you can chat with any specialized assistant that has been created for
              you.
            </p>
            <p>Choose an assistant from the dropdown to begin.</p>
            {#if termOfService}
              <SvelteMarkdownWrapper source={termOfService} />
            {/if}
          {/if}
        </div>
      {/each}

      {#if lastMessageErrored}
        <div class="flex items-center gap-2">
          <span>Ett fel uppstod ⚠️️</span>
          <button class="btn btn-link active:opacity-60" on:click={retryLastMessage}>
            Försök igen
          </button>
        </div>
      {/if}

      <span class="loading loading-spinner" class:opacity-0={!isRequestRunning} />
    </div>
  </div>

  <!-- Bottom controls -->
  <div class="z-10 p-3">
    <form class="h-full w-full" on:submit={scrollContentToBottom}>
      <fieldset
        disabled={(!selectedAssistantId || !!lastMessageErrored) && !initialState}
        class="h-full"
      >
        <div class="flex h-full w-full items-end gap-2">
          <div class="flex h-full w-full grow flex-col gap-1.5">
            <TokenCounter
              bind:this={tokenCounter}
              maxTokens={initialState?.max_tokens ?? selectedAssistant?.maxTokens ?? -1}
              bind:exceededTokenCount={exceededTokenCount}
            />
            <textarea
              name="message"
              bind:value={currentMessageInput}
              on:keydown={handleTextareaKeypress}
              class="textarea textarea-bordered h-full grow"
              class:textarea-error={exceededTokenCount}
            />
          </div>
          <Button
            disabled={exceededTokenCount}
            on:click={formButtonClick}
            label=""
            iconSrc={formButtonIcon}
          />
        </div>
      </fieldset>
    </form>
  </div>
</div>
