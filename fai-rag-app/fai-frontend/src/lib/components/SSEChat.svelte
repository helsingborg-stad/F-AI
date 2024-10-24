<script lang="ts">
  import Button from './Button.svelte'
  import ChatBubble from './ChatBubble.svelte'
  import SvelteMarkdownWrapper from '$lib/components/SvelteMarkdownWrapper.svelte'
  import SVG from '$lib/components/SVG.svelte'
  import { findLastIndex } from '../../util/array'

  interface IncomingMessage {
    timestamp: string
    source?: string
    content: string
  }

  interface ChatMessage {
    id: string
    user: string
    content: string
    timestamp: string
    isSelf: boolean
  }

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
  let messages: ChatMessage[] = []
  let currentMessageInput: string = ''
  let eventSource: EventSource | null = null

  let contentScrollDiv: Element
  let isContentAtBottom: Boolean = true
  let lastMessageErrored: Boolean = false

  let tokenCount = -1
  let tokenTimeoutHandle = -1
  $: maxTokens = initialState?.max_tokens ?? selectedAssistant?.maxTokens ?? -1
  $: invalidInputLength = maxTokens > 0 && tokenCount > maxTokens
  $: {
    if (selectedAssistantId) {
      tokenCount = -1
    }
  }

  $: console.log(initialState)

  // TODO: send assistant_id as well
  function updateTokenCount(text: string, conversationId: string | null, assistantId: string | null) {
    console.log(text, conversationId, assistantId)
    fetch(`/api/count-tokens`, {
        method: 'POST',
        body: JSON.stringify({ text, conversation_id: conversationId, assistant_id: assistantId }),
        headers: {
          'Content-Type': 'application/json',
        },
      },
    ).then(res => res.json())
      .then(res => {
        tokenCount = res?.count ?? -1
      })
      .catch(() => {
        tokenCount = -1
      })
      .finally(() => {
        tokenTimeoutHandle = -1
      })
  }

  function queueUpdateTokenCount(text: string, conversationId: string | null, assistantId: string | null) {
    clearTimeout(tokenTimeoutHandle)
    tokenTimeoutHandle = setTimeout(() => updateTokenCount(text, conversationId, assistantId), 1000)
  }

  $: activeConversationId && queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)
  $: messages && activeConversationId && queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)
  $: selectedAssistantId && queueUpdateTokenCount(currentMessageInput, activeConversationId, selectedAssistantId)

  $: {
    if (initialState) {
      activeConversationId = initialState.chat_id
      messages = initialState.history.map(toChatMessage)
    } else {
      messages = []
    }
  }

  function updateBottomCheck() {
    const margin = 50
    isContentAtBottom =
      contentScrollDiv &&
      contentScrollDiv.scrollHeight -
      contentScrollDiv.scrollTop -
      contentScrollDiv.clientHeight <=
      margin
  }

  $: selectedAssistant = assistants.find((a) => a.id === selectedAssistantId) || null
  $: contentScrollDiv &&
  messages &&
  messages.length > 0 &&
  isContentAtBottom &&
  scrollContentToBottom()
  $: lastMessageErrored && setTimeout(scrollContentToBottom, 100)

  const scrollToBottom = (node: Element) => {
    node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
  }

  function scrollContentToBottom() {
    scrollToBottom(contentScrollDiv)
  }

  function toChatMessage(sse: IncomingMessage): ChatMessage {
    return {
      id: sse.timestamp,
      user: sse.source ?? '',
      content: sse.content ?? '',
      timestamp: sse.timestamp,
      isSelf: sse.source == 'user',
    }
  }

  function clearChat() {
    messages = []
    activeConversationId = null
    lastMessageErrored = false
  }

  function closeSSE() {
    eventSource?.close()
    eventSource = null
  }

  function createSSE(question: string) {
    if (question.length == 0) return
    currentMessageInput = ''

    messages = [
      ...messages,
      {
        id: `self${messages.length}`,
        isSelf: true,
        user: 'Me',
        content: question,
        timestamp: new Date().toISOString(),
      },
      {
        id: `placeholder${messages.length}`,
        isSelf: false,
        user: '',
        content: '',
        timestamp: '',
      },
    ]

    closeSSE()

    fetch('/api/sse/chat/question', {
      method: 'POST',
      body: JSON.stringify({ question }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((response) => {
        const questionId = response.id

        const fullEndpoint = activeConversationId
          ? `/api/sse/chat/stream/continue/${activeConversationId}?stored_question_id=${questionId}`
          : `/api/sse/chat/stream/new/${selectedAssistant!.project}/${selectedAssistant!.id}?stored_question_id=${questionId}`

        eventSource = new EventSource(fullEndpoint)

        eventSource.onerror = (e) => {
          console.error(e)
          lastMessageErrored = true
          closeSSE()
        }

        eventSource.addEventListener('message_end', () => {
          closeSSE()
        })

        eventSource.addEventListener('conversation_id', (e) => {
          activeConversationId = e.data
        })

        eventSource.addEventListener('exception', () => {
          lastMessageErrored = true
        })

        eventSource.addEventListener('message', (e) => {
          try {
            const bytes = Uint8Array.from(atob(e.data), (m) => m.codePointAt(0)!)
            const jsonString = new TextDecoder().decode(bytes)
            const messagePayload = JSON.parse(jsonString) as IncomingMessage
            const chatMessage = toChatMessage(messagePayload)

            messages = [
              ...messages.slice(0, -1),
              {
                ...messages.at(-1),
                ...chatMessage,
                content: messages.at(-1)!.content + chatMessage.content,
              },
            ]
          } catch (ex) {
            console.error('Failed to parse raw message', ex, e)
            closeSSE()
          }
        })
      })
  }

  function handleTextareaKeypress(event: KeyboardEvent) {
    if (event.key == 'Enter' && !event.shiftKey) {
      event.preventDefault()
      if (!invalidInputLength) createSSE(currentMessageInput)
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
    if (eventSource) {
      closeSSE()
      return
    }

    createSSE(currentMessageInput)
  }

  $: formButtonIcon = eventSource
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

      <span class="loading loading-spinner" class:opacity-0={!eventSource} />
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
            <span
              class:hidden={maxTokens <= 0}
              class="block text-right text-xs">
              {#if tokenTimeoutHandle >= 0}
                ...
              {:else}
                {tokenCount}/{maxTokens}
              {/if}
            </span>
            <textarea
              name="message"
              bind:value={currentMessageInput}
              on:keydown={handleTextareaKeypress}
              class="textarea textarea-bordered h-full grow"
              class:textarea-error={invalidInputLength}
            />
          </div>
          <Button
            disabled={invalidInputLength}
            on:click={formButtonClick}
            label=""
            iconSrc={formButtonIcon}
          />
        </div>
      </fieldset>
    </form>
  </div>
</div>
