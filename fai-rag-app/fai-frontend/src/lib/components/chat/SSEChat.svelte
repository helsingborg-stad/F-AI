<script lang="ts">
  import Button from '../Button.svelte'
  import ChatBubble from '../ChatBubble.svelte'
  import SvelteMarkdownWrapper from '$lib/components/SvelteMarkdownWrapper.svelte'
  import SVG from '$lib/components/SVG.svelte'
  import { findLastIndex } from '../../../util/array'
  import TokenCounter from '$lib/components/chat/TokenCounter.svelte'
  import { type ChatMessage, type IncomingMessage, incomingMessageToChatMessage, SSE } from '$lib/components/chat/SSE'
  import AttachedFile from '$lib/components/chat/AttachedFile.svelte'

  interface Assistant {
    id: string
    name: string
    project: string
    description: string
    sampleQuestions: string[]
    maxTokens: number
    allowInlineFiles: boolean
  }

  interface InitialState {
    chat_id: string
    max_tokens: number
    history: IncomingMessage[]
    allow_inline_files: boolean
  }

  interface InlineFile {
    file: File
    status: 'parsing' | 'done' | 'error'
    parsed_content: string | null
  }

  const inlineFileAttachedFileStatusStateMap = {
    'parsing': 'pending',
    'done': 'valid',
    'error': 'invalid',
  } as const

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

  function redactDocumentText(fullContent: string): string {
    const beginMatcher = /\[BEGIN DOCUMENT (.*)]/
    const match = beginMatcher.exec(fullContent)
    if (match) {
      const endTag = '\n[END DOCUMENT]\n'
      const endIndex = fullContent.indexOf(endTag, match.index)
      if (endIndex !== -1) {
        const redacted = fullContent.slice(0, match.index)
          + `[document ${match[1]}]`
          + fullContent.slice(endIndex + endTag.length)
        return redactDocumentText(redacted)
      }
    }
    return fullContent
  }

  function getFullMessageInput(question: string) {
    let fullQuestion = question

    const fileIds = Object.keys(inlineFiles)
    if (fileIds.length > 0) {
      const combinedContent = fileIds
        .map(id => `[BEGIN DOCUMENT ${inlineFiles[id].file.name}]\n${inlineFiles[id].parsed_content}\n[END DOCUMENT]`)
        .join('\n\n')
      fullQuestion = combinedContent + '\n\n' + fullQuestion
    }

    return fullQuestion
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
    sse.create(getFullMessageInput(question), activeConversationId, selectedAssistant?.project, selectedAssistant?.id)
    currentMessageInput = ''
    inlineFiles = {}
  }

  function closeSSE() {
    sse.close()
  }

  /** Token Counting */
  let exceededTokenCount: false
  let tokenCounter: TokenCounter
  $: activeConversationId && tokenCounter?.queueUpdateTokenCount(getFullMessageInput(currentMessageInput), activeConversationId, selectedAssistantId)
  $: messages && activeConversationId && tokenCounter?.queueUpdateTokenCount(getFullMessageInput(currentMessageInput), activeConversationId, selectedAssistantId)
  $: selectedAssistantId && tokenCounter?.queueUpdateTokenCount(getFullMessageInput(currentMessageInput), activeConversationId, selectedAssistantId)
  $: inlineFiles && tokenCounter?.queueUpdateTokenCount(getFullMessageInput(currentMessageInput), activeConversationId, selectedAssistantId)

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

  /** File inlining */
  let inlineFileInput: HTMLInputElement
  let inlineFiles: { [id: string]: InlineFile } = {}
  let allowInlineFiles = false
  let anyInvalidFiles: boolean = false
  $: anyInvalidFiles = Object.keys(inlineFiles).some(i => inlineFiles[i].status !== 'done')
  $: allowInlineFiles = !!selectedAssistant?.allowInlineFiles || !!initialState?.allow_inline_files

  function parseInlineFile(id: string) {
    if (!inlineFiles[id]) {
      return
    }

    const formData = new FormData()
    formData.append('file', inlineFiles[id].file)

    inlineFiles[id].status = 'parsing'
    fetch('/api/document/parse', {
      method: 'POST',
      body: formData,
    }).then(r => {
      if (!r.ok) {
        throw Error(`${r.status} ${r.statusText}`)
      }
      return r.text()
    })
      .then(data => {
        console.log('data', data)
        inlineFiles[id].parsed_content = data
        inlineFiles[id].status = 'done'
      })
      .catch(err => {
        inlineFiles[id].status = 'error'
        console.error(`failed to parse`, err, inlineFiles[id])
      })
  }

  function showInlineFileDialog() {
    inlineFileInput.click()
  }

  function inlineFilesChanged(ev: Event) {
    const element = ev.currentTarget as HTMLInputElement
    const files: File[] = element.files ? Array.from(element.files) : []
    inlineFiles = files.reduce((acc, file) => ({
      ...acc,
      [`${file.name}_${file.lastModified}`]: {
        file,
        status: 'parsing',
        parsed_content: null,
      },
    }), {})

    Object.keys(inlineFiles).forEach(parseInlineFile)
  }

  function removeInlineFile(id: string) {
    delete inlineFiles[id]
    inlineFiles = { ...inlineFiles }
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
      if (!exceededTokenCount && !anyInvalidFiles) createSSE(currentMessageInput)
    }
  }

  function formatMessageForMarkdown(content: string): string {
    return content.replace(/\n/g, `\n\n  `)
  }

  function formatSelfMessage(content: string): string {
    return redactDocumentText(content)
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
  class:grid-rows-[6rem_1fr_12rem]={!initialState}
  class:grid-rows-[1fr_12rem]={initialState}
>
  <!-- Floating controls -->
  <div
    class="absolute inset-x-0 bottom-52 z-10 flex justify-center transition"
    class:translate-y-40={isContentAtBottom}
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
            ? formatSelfMessage(message.content)
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
  <div class="z-10 p-3 bg-white">
    <div
      class="w-full max-w-full overflow-hidden h-full grid grid-cols-[auto_1fr_auto] grid-rows-[auto_auto_1fr] gap-1">
      <div class="w-full h-full" />
      <div class="w-full h-full">
        <div class="flex gap-2 w-full">
          {#each Object.keys(inlineFiles) as fileId}
            <AttachedFile
              title={inlineFiles[fileId].file.name}
              onRemove={() => removeInlineFile(fileId)}
              state={inlineFileAttachedFileStatusStateMap[inlineFiles[fileId].status]}
            />
          {/each}
        </div>
      </div>
      <div class="w-full h-full" />

      <div class="w-full h-full" />
      <div class="w-full h-full">
        <TokenCounter
          bind:this={tokenCounter}
          maxTokens={initialState?.max_tokens ?? selectedAssistant?.maxTokens ?? -1}
          bind:exceededTokenCount={exceededTokenCount}
        />
      </div>
      <div class="w-full h-full" />

      {#if allowInlineFiles}
        <div class="w-full h-full flex items-end">
          <Button
            on:click={showInlineFileDialog}
            label=""
            iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXBhcGVyY2xpcCI+PHBhdGggZD0ibTIxLjQ0IDExLjA1LTkuMTkgOS4xOWE2IDYgMCAwIDEtOC40OS04LjQ5bDguNTctOC41N0E0IDQgMCAxIDEgMTggOC44NGwtOC41OSA4LjU3YTIgMiAwIDAgMS0yLjgzLTIuODNsOC40OS04LjQ4Ii8+PC9zdmc+"
          />
          <div class="hidden">
            <input
              bind:this={inlineFileInput}
              type="file"
              multiple
              on:change={inlineFilesChanged}
            />
          </div>
        </div>
      {/if}

      <div
        class="w-full h-full"
        class:col-span-2={!allowInlineFiles}
      >
        <textarea
          name="message"
          bind:value={currentMessageInput}
          on:keydown={handleTextareaKeypress}
          class="textarea textarea-bordered h-full w-full grow leading-tight"
          placeholder="Message"
          class:textarea-error={exceededTokenCount}
        />
      </div>
      <div class="w-full h-full flex items-end">
        <Button
          disabled={exceededTokenCount || anyInvalidFiles}
          on:click={formButtonClick}
          label=""
          iconSrc={formButtonIcon}
        />
      </div>
    </div>
  </div>
</div>
