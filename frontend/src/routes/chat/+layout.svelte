<script lang="ts">
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import { page } from '$app/state'
  import { goto } from '$app/navigation'
  import { type RealtimeChatMessage, sendChatMessage } from '$lib/chat/chat.js'
  import dayjs from 'dayjs'
  import type { LayoutData } from './$types.js'

  interface Props {
    data: LayoutData
  }

  const { data }: Props = $props()


  let selectedAssistantId = $state('')

  // Clear state when changing assistant
  $effect(() => {
    if (selectedAssistantId !== '') {
      goto(`/chat/`, {
        replaceState: false,
        noScroll: true,
        keepFocus: true,
      })
    }
  })


  const conversationId: string | undefined = $derived(page.params.conversationId)

  let messages = $state(data.messages)

  // Used to set messages when going from one chat to another when components are not re-mounted
  $effect(() => {
    messages = data.messages
  })

  async function sendMessage(message: string) {
    const onAddMessage = (message: RealtimeChatMessage) => messages = [...messages, { timestamp: dayjs().toISOString(), ...message }]

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
    }

    await sendChatMessage(message, selectedAssistantId, conversationId, onAddMessage, onUpdateLastMessage, onGoto, onError)
  }
</script>

<ChatLayout
  {messages}
  assistants={data.assistants}
  inputPlaceholder="Fråga Folkets AI"
  onSubmitMessage={sendMessage}
  bind:selectedAssistantId={selectedAssistantId}
  {conversationId}
>
</ChatLayout>
