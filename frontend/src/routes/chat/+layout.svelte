<script lang="ts">
  import ChatLayout from '$lib/layouts/ChatLayout.svelte'
  import { page } from '$app/state'
  import { goto } from '$app/navigation'
  import { type RealtimeChatMessage, sendChatMessage } from '$lib/chat/chat.js'
  import type { Snippet } from 'svelte'
  import dayjs from 'dayjs'

  interface Message {
    timestamp: string
    source: string
    message: string
  }

  interface Props {
    data: {
      messages: Message[]
    }
    children: Snippet
  }

  const { data, children }: Props = $props()

  const conversationId: string | undefined = $derived(page.params.conversationId)

  let messages = $state(data.messages)

  // Used to set messages when going from one chat to another when components are not re-mounted
  $effect(() => {
    messages = data.messages
    console.log('reset messages', data.messages)
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

    await sendChatMessage(message, conversationId, onAddMessage, onUpdateLastMessage, onGoto, onError)
  }
</script>

<ChatLayout
  {messages}
  inputPlaceholder="Fråga Folkets AI"
  onSubmitMessage={sendMessage}
>
  {@render children()}
</ChatLayout>
