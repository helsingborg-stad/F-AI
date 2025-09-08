<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import { page } from '$app/state'
  import { goto, invalidateAll } from '$app/navigation'
  import dayjs from 'dayjs'
  import type { LayoutData } from './$types.js'
  import { useChatMachine } from '$lib/chat/chat.js'
  import { type FileWithState, useInlineFiles } from '$lib/files/useInlineFiles.js'
  import type { IFrontendConversationMessage } from '$lib/types.js'

  interface Props {
    data: LayoutData
  }

  const { data }: Props = $props()

  let selectedAssistantId = $state('')
  let enabledFeatures: string[] = $state([])

  const chatMachine = useChatMachine()
  const { state: chatState } = chatMachine

  function startNewChat() {
    goto(`/chat/`, {
      replaceState: false,
      noScroll: true,
      keepFocus: true,
    })
  }

  $effect(() => {
    if (data.conversationContext && data.conversationContext.assistantId) {
      selectedAssistantId = data.conversationContext.assistantId
    }
  })

  // Clear state when manually changing assistant
  $effect(() => {
    if (
      selectedAssistantId !== '' &&
      selectedAssistantId !== data.conversationContext?.assistantId
    ) {
      startNewChat()
    }
  })

  const conversationId: string | undefined = $derived(page.params.conversationId)

  let messages: IFrontendConversationMessage[] = $state(
    data.conversationContext.messages.map(redactMessage),
  )

  // Track previous conversation ID to detect actual conversation switches
  let previousConversationId = $state<string | undefined>(undefined)

  // Used to set messages when going from one chat to another when components are not re-mounted
  $effect(() => {
    const currentConversationId = page.params.conversationId

    // Stop chat machine when switching between different existing conversations
    if (
      previousConversationId &&
      currentConversationId &&
      previousConversationId !== currentConversationId
    ) {
      chatMachine.stop()
    }

    previousConversationId = currentConversationId
    messages = data.conversationContext.messages.map(redactMessage)
  })

  chatMachine.lastMessage.subscribe((message) => {
    messages = [
      ...messages.slice(0, messages.length - 1),
      {
        timestamp: dayjs().toISOString(),
        source: message.source,
        message: message.message,
        reasoning: message.reasoning,
      },
    ].map(redactMessage)
  })

  chatMachine.conversationId.subscribe((newConversationId) => {
    if (newConversationId != null) {
      const cachedMessages = messages
      goto(`/chat/${newConversationId}`, {
        replaceState: false,
        noScroll: true,
        keepFocus: true,
      })
        .then(() => (messages = cachedMessages))
        .catch((e) => console.error('goto failed', e))
    }
  })

  chatMachine.lastError.subscribe((error) => {
    if (error != null) {
      messages = [
        ...messages.slice(0, messages.length - 1),
        {
          timestamp: dayjs().toISOString(),
          source: 'error',
          message: error,
          reasoning: '',
        },
      ].map(redactMessage)
    }
  })

  function redactDocumentText(inMessage: string): string {
    // TODO: move to ChatMachine? For best results requires moving full message state to ChatMachine (see conversation edit wip branch)
    const beginMatcher = /\[BEGIN (\w+)(?: (.*))?]/
    const match = beginMatcher.exec(inMessage)
    if (match) {
      const tagName = match[1]
      const endTag = `[END ${tagName}]`
      const endIndex = inMessage.indexOf(endTag, match.index)
      if (endIndex !== -1) {
        const redacted =
          inMessage.slice(0, match.index) +
          // `[${match[1]} ${match[2]}]` +
          inMessage.slice(endIndex + endTag.length)
        return redactDocumentText(redacted)
      }
    }
    return inMessage
  }

  function redactMessage(
    inMessage: IFrontendConversationMessage,
  ): IFrontendConversationMessage {
    return {
      ...inMessage,
      message: redactDocumentText(inMessage.message),
    }
  }

  function sendMessage(message: string) {
    messages = [
      ...messages,
      { timestamp: dayjs().toISOString(), source: 'user', message, reasoning: '' },
      {
        timestamp: dayjs().toISOString(),
        source: 'assistant',
        message: '',
        reasoning: '',
      },
    ].map(redactMessage)

    const filteredFiles = inlineFiles.filter((f) => f.state === 'valid')

    if (filteredFiles.length > 0) {
      message =
        message +
        '\n\n[BEGIN INSTRUCTIONS]\n\n(Try to answer the question(s) with the document contents provided below.)\n\n[END INSTRUCTIONS]\n\n' +
        inlineFiles
          .map(
            (f) =>
              `[BEGIN DOCUMENT ${f.file.name}]\n\n${f.parsedContents ?? ''}\n\n[END DOCUMENT]\n`,
          )
          .join('\n\n')
    }

    inlineFilesHook.setFiles([])

    chatMachine
      .sendMessage(message, selectedAssistantId, conversationId ?? null, {
        withFeatures: enabledFeatures,
      })
      .catch((e) => console.error('chatMachine.sendMessage failed', e))
  }

  function deleteConversation(id: string) {
    fetch(`/api/conversation/delete`, {
      method: 'POST',
      body: JSON.stringify({ id }),
    })
      .then(() => {
        if (id === conversationId) {
          return goto(`/chat/`, {})
        }
      })
      .then(invalidateAll)
  }

  function renameConversation(conversationId: string, title: string) {
    fetch(`/api/conversation/${conversationId}/title`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title }),
    })
      .then(() => {
        if (conversationId === conversationId) {
          return goto(`/chat/`, {})
        }
      })
      .then(invalidateAll)
  }

  const assistantIdFromQuery = $derived(page.url.searchParams.get('assistant_id'))
  $effect(() => {
    if (assistantIdFromQuery) {
      selectedAssistantId = assistantIdFromQuery
    } else if (data.conversationContext && data.conversationContext.assistantId) {
      selectedAssistantId = data.conversationContext.assistantId
    }
  })

  const inlineFilesHook = useInlineFiles()
  let inlineFiles: FileWithState[] = $state([])
  inlineFilesHook.files.subscribe((files) => {
    inlineFiles = files
  })
  let canChangeFiles = $state(true)
  inlineFilesHook.canChangeFiles.subscribe((canChange) => {
    canChangeFiles = canChange
  })

  function changeFiles(newFiles: File[]) {
    const oldSet = new Set(inlineFiles.map((f) => f.id))
    const newSet = new Set(newFiles.map((f) => inlineFilesHook.getFileId(f)))

    const removedFiles = [...oldSet].filter((f) => !newSet.has(f))
    const addedFiles = [...newSet].filter((f) => !oldSet.has(f))

    if (addedFiles.length == 0) {
      removedFiles.forEach(inlineFilesHook.removeFile)
    } else {
      inlineFilesHook.setFiles(newFiles)
    }
  }
</script>

<ChatLayout
  canChat={data.canChat}
  messages={messages.map((m, i) => ({
    ...m,
    showLoader: i === messages.length - 1 && !['idle', 'error'].includes($chatState),
  }))}
  assistants={data.assistants}
  conversations={data.conversations}
  inputPlaceholder={m.chat_input_placeholder({ applicationName: 'Folkets AI' })}
  onSubmitMessage={sendMessage}
  bind:selectedAssistantId
  {conversationId}
  onRenameConversation={renameConversation}
  onDeleteConversation={deleteConversation}
  onStartNewChat={startNewChat}
  onStopChat={chatMachine.stop}
  chatStateIdle={$chatState === 'idle' || $chatState === 'error'}
  bind:enabledFeatures
  {inlineFiles}
  {canChangeFiles}
  onFilesChanged={changeFiles}
/>
