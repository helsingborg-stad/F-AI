<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
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
    if (selectedAssistantId !== '' && selectedAssistantId !== data.conversationContext?.assistantId) {
      startNewChat()
    }
  })

  const conversationId: string | undefined = $derived(page.params.conversationId)

  let messages = $state(data.conversationContext.messages)

  // Track previous conversation ID to detect actual conversation switches
  let previousConversationId = $state<string | undefined>(undefined)

  // Used to set messages when going from one chat to another when components are not re-mounted
  $effect(() => {
    const currentConversationId = page.params.conversationId

    // Stop chat machine when switching between different existing conversations
    if (previousConversationId && currentConversationId && previousConversationId !== currentConversationId) {
      chatMachine.stop()
    }

    previousConversationId = currentConversationId
    messages = data.conversationContext.messages
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
          reasoning: '',
        },
      ]
    }
  })

  function sendMessage(message: string) {
    messages = [
      ...messages,
      { timestamp: dayjs().toISOString(), source: 'user', message, reasoning: '' },
      { timestamp: dayjs().toISOString(), source: 'assistant', message: '', reasoning: '' },
    ]

    chatMachine.sendMessage(message, selectedAssistantId, conversationId ?? null, {
      withFeatures: enabledFeatures,
    })
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

  function renameConversation(conversationId: string, title: string) {
    fetch(`/api/conversation/${conversationId}/title`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      },
    )
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
</script>

<ChatLayout
  canChat={data.canChat}
  messages={messages.map((m, i) => ({
    ...m,
    showLoader: i === messages.length - 1 && !['idle', 'error'].includes($chatState),
  }))}
  assistants={data.assistants}
  conversations={data.conversations}
  inputPlaceholder={m.chat_input_placeholder({ applicationName: 'Folkets AI'})}
  onSubmitMessage={sendMessage}
  bind:selectedAssistantId
  {conversationId}
  onRenameConversation={renameConversation}
  onDeleteConversation={deleteConversation}
  onStartNewChat={startNewChat}
  onStopChat={chatMachine.stop}
  chatStateIdle={$chatState === 'idle'}
  bind:enabledFeatures
>
</ChatLayout>

