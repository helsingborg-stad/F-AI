<script lang="ts">
  import Button from './Button.svelte'
  import ChatBubble from './ChatBubble.svelte'
  import SvelteMarkdown from 'svelte-markdown'
  import SVG from '$lib/components/SVG.svelte'
  import { findLastIndex } from '../../util/array'

  interface SSEMessage {
    type: string
    timestamp: string
    source: string | null
    content: string | null
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
  }

  export let assistants: Assistant[]

  let selectedAssistantId: string
  let selectedAssistant: Assistant | null = null
  let activeConversationId: string | null = null
  let messages: ChatMessage[] = []
  let currentMessageInput: string = ''
  let eventSource: EventSource | null = null

  let contentScrollDiv: Element
  let isContentAtBottom: Boolean = true
  let lastMessageErrored: Boolean = false

  function updateBottomCheck() {
    const margin = 100
    isContentAtBottom = contentScrollDiv && contentScrollDiv.scrollHeight - contentScrollDiv.scrollTop - contentScrollDiv.clientHeight <= margin
  }

  $: selectedAssistant = assistants.find((a) => a.id === selectedAssistantId) || null
  $: contentScrollDiv &&
  messages &&
  messages.length > 0 &&
  scrollContentToBottom()
  $: lastMessageErrored && setTimeout(scrollContentToBottom, 100)

  const scrollToBottom = (node: Element) => {
    node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
  }

  function scrollContentToBottom() {
    scrollToBottom(contentScrollDiv)
  }

  function toChatMessage(sse: SSEMessage): ChatMessage {
    return {
      id: sse.timestamp,
      user: sse.source ?? '',
      content: sse.content ?? '',
      timestamp: sse.timestamp,
      isSelf: false,
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

    const fullEndpoint = activeConversationId
      ? `/api/sse/chat/stream/continue/${activeConversationId}?question=${question}`
      : `/api/sse/chat/stream/new/${selectedAssistant!.project}/${selectedAssistant!.id}?question=${question}`

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
        const messagePayload = JSON.parse(jsonString) as SSEMessage
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
  }

  function handleTextareaKeypress(event: KeyboardEvent) {
    if (event.key == 'Enter' && !event.shiftKey) {
      event.preventDefault()
      createSSE(currentMessageInput)
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
    const lastUserMessageIndex = findLastIndex(messages, m => m.isSelf)
    const lastQuestion = messages[lastUserMessageIndex].content
    messages = messages.slice(0, lastUserMessageIndex)
    createSSE(lastQuestion)
  }
</script>

<div class="w-full lg:w-[calc(100%-20rem)] absolute top-16 bottom-0 overflow-hidden grid grid-rows-[6rem_1fr_7rem]">
  <!-- Floating controls -->
  <div
    class="absolute inset-x-0 bottom-32 translate-y-20 flex justify-center z-10 transition"
    class:translate-y-0={!isContentAtBottom}
  >
    <button
      on:click={scrollContentToBottom}
      class="bg-white rounded-full shadow p-2 hover:bg-gray-100 active:scale-95 transition"
    >
      <SVG
        width="24"
        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWFycm93LWJpZy1kb3duLWRhc2giPjxwYXRoIGQ9Ik0xNSA1SDkiLz48cGF0aCBkPSJNMTUgOXYzaDRsLTcgNy03LTdoNFY5eiIvPjwvc3ZnPg==" />
    </button>
  </div>

  <!-- Top controls -->
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

  <!-- Content -->
  <div
    class="overflow-y-scroll flex justify-center"
    bind:this={contentScrollDiv}
    on:scroll={updateBottomCheck}
  >
    <div class="max-w-prose w-full h-fit">
      {#each messages as message (message.id)}
        <ChatBubble
          content={formatMessageForMarkdown(message.content)}
          isSelf={message.isSelf}
        />
      {:else}
        <div class="prose text-center">
          {#if selectedAssistant}
            <SvelteMarkdown source={selectedAssistant.description} />

            <div class="flex gap-2 max-w-full flex-wrap justify-center">
              {#each selectedAssistant.sampleQuestions as question}
                <button
                  class="btn btn-outline"
                  on:click={() => askSampleQuestion(question)}>{question}</button
                >
              {/each}
            </div>
          {:else}
            <p>
              Here you can chat with any specialized assistant that has been created for
              you.
            </p>
            <p>Choose an assistant from the dropdown to begin.</p>
          {/if}
        </div>
      {/each}

      {#if lastMessageErrored}
        <div class="flex items-center gap-2">
          <span>Ett fel uppstod ⚠️️</span>
          <button class="btn btn-link active:opacity-60" on:click={retryLastMessage}>Försök igen</button>
        </div>
      {/if}

      <span class="loading loading-spinner" class:opacity-0={!eventSource} />
    </div>
  </div>

  <!-- Bottom controls -->
  <div class="p-3 z-10">
    <form class="h-full w-full" on:submit={scrollContentToBottom}>
      <fieldset disabled={!selectedAssistantId || !!lastMessageErrored} class="h-full">
        <div class="flex h-full w-full items-end gap-2">
          <textarea
            name="message"
            bind:value={currentMessageInput}
            on:keydown={handleTextareaKeypress}
            class="textarea textarea-bordered h-full grow"
          />
          <Button
            on:click={() => createSSE(currentMessageInput)}
            label=""
            iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlbmQiPjxwYXRoIGQ9Im0yMiAyLTcgMjAtNC05LTktNFoiLz48cGF0aCBkPSJNMjIgMiAxMSAxMyIvPjwvc3ZnPg=="
          />
        </div>
      </fieldset>
    </form>
  </div>
</div>
