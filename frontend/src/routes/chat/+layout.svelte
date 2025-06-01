<script lang="ts">
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import { page } from '$app/state'
  import { goto, invalidateAll } from '$app/navigation'
  import { type ChatController, type RealtimeChatMessage, sendChatMessage } from '$lib/chat/chat.js'
  import dayjs from 'dayjs'
  import type { LayoutData } from './$types.js'

  interface Props {
    data: LayoutData
  }

  const { data }: Props = $props()

  let selectedAssistantId = $state('')
  let currentChatController = $state<ChatController | null>(null)
  let chatStateIdle = $state(true)

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
    if (selectedAssistantId !== '' && selectedAssistantId !== data.conversationContext?.assistantId) {
      startNewChat()
    }
  })

  const conversationId: string | undefined = $derived(page.params.conversationId)

  let messages = $state(data.conversationContext.messages)

  // Used to set messages when going from one chat to another when components are not re-mounted
  $effect(() => {
    messages = data.conversationContext.messages
  })

  async function sendMessage(message: string) {
    const onAddMessage = (message: RealtimeChatMessage) => {
      chatStateIdle = false
      messages = [...messages, { timestamp: dayjs().toISOString(), ...message }]
    }

    const onUpdateLastMessage = (message: RealtimeChatMessage) => messages = [
      ...messages.slice(0, messages.length - 1),
      {
        timestamp: dayjs().toISOString(),
        source: message.source,
        message: message.message,
      },
    ]

    const onGoto = (url: string) => {
      const cachedMessages = messages
      goto(url, {
        replaceState: false,
        noScroll: true,
        keepFocus: true,
      })
        .then(() => messages = cachedMessages)
        .catch(e => console.error('goto failed', e))
    }

    const onError = (error: string) => {
      onUpdateLastMessage({ source: 'error', message: error })
      currentChatController = null
      chatStateIdle = true
    }

    const onMessageEnd = () => {
      chatStateIdle = true
    }

    currentChatController = await sendChatMessage(
      message,
      selectedAssistantId,
      conversationId,
      onAddMessage,
      onUpdateLastMessage,
      onGoto,
      onError,
      onMessageEnd,
    )
  }

  function stopChat() {
    if (currentChatController) {
      currentChatController.close()
      currentChatController = null
      chatStateIdle = true
    }
  }

  function deleteConversation(id: string) {
    fetch(`/api/conversation/delete`,
      {
        method: 'POST',
        body: JSON.stringify({ id }),
      },
    )
      .then(() => {
        if (id === conversationId) {
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
</script>

<ChatLayout
  canChat={data.canChat}
  {messages}
  assistants={data.assistants}
  conversations={data.conversations}
  inputPlaceholder="Fråga Folkets AI"
  onSubmitMessage={sendMessage}
  bind:selectedAssistantId
  {conversationId}
  onDeleteConversation={deleteConversation}
  onStartNewChat={startNewChat}
  onStopChat={stopChat}
  {chatStateIdle}
>
</ChatLayout>
