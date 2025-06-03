<script lang="ts">
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import { page } from '$app/state'
  import { goto, invalidateAll } from '$app/navigation'
  import dayjs from 'dayjs'
  import type { LayoutData } from './$types.js'
  import { useChatMachine } from '$lib/chat/chat.js'

  interface Props {
    data: LayoutData
  }

  const { data }: Props = $props()

  let selectedAssistantId = $state('')

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

  chatMachine.lastMessage.subscribe((message) => {
    messages = [
      ...messages.slice(0, messages.length - 1),
      {
        timestamp: dayjs().toISOString(),
        source: message.source,
        message: message.message,
      },
    ]
  })

  chatMachine.conversationId.subscribe((newConversationId) => {
    if (newConversationId != null) {
      const cachedMessages = messages
      goto(`/chat/${newConversationId}`, {
        replaceState: false,
        noScroll: true,
        keepFocus: true,
      })
        .then(() => messages = cachedMessages)
        .catch(e => console.error('goto failed', e))
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
        },
      ]
    }
  })

  function sendMessage(message: string) {
    messages = [
      ...messages,
      { timestamp: dayjs().toISOString(), source: 'user', message },
      { timestamp: dayjs().toISOString(), source: 'assistant', message: '' },
    ]

    chatMachine.sendMessage(message, selectedAssistantId, conversationId ?? null)
      .catch(e => console.error('chatMachine.sendMessage failed', e))
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
  messages={messages.map((m, i) => ({
    ...m,
    showLoader: i === messages.length - 1 && !['idle', 'error'].includes($chatState),
  }))}
  assistants={data.assistants}
  conversations={data.conversations}
  inputPlaceholder="Fråga Folkets AI"
  onSubmitMessage={sendMessage}
  bind:selectedAssistantId
  {conversationId}
  onDeleteConversation={deleteConversation}
  onStartNewChat={startNewChat}
  onStopChat={chatMachine.stop}
  chatStateIdle={$chatState === 'idle'}
>
</ChatLayout>
