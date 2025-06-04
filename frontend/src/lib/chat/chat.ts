import { type Readable, type Writable, writable } from 'svelte/store'

export interface ChatMessage {
  source: string
  message: string
}

export type ChatMachineState = 'idle' | 'sending' | 'waiting' | 'responding' | 'error'

export interface ChatMachine {
  state: Readable<ChatMachineState>
  conversationId: Readable<string | null>
  lastMessage: Readable<ChatMessage>
  lastError: Readable<string | null>
  sendMessage: (message: string, assistantId: string | null, conversationId: string | null) => Promise<void>
  stop: () => void
}

export function useChatMachine(): ChatMachine {
  let es: EventSource | null = null

  const state: Writable<ChatMachineState> = writable('idle')
  const lastConversationId: Writable<string | null> = writable(null)
  const lastMessage: Writable<ChatMessage> = writable({ source: '', message: '' })
  const lastError: Writable<string | null> = writable(null)
  let cancelAnyInProgressCalls: boolean = false

  const close = () => {
    if (es) {
      es.close()
      es = null
    }
    state.set('idle')
    cancelAnyInProgressCalls = true
  }

  return {
    state,
    conversationId: lastConversationId,
    lastMessage,
    lastError,

    async sendMessage(message: string, assistantId: string | null, conversationId: string | null) {
      if (es) {
        return
      }

      state.set('sending')
      lastConversationId.set(conversationId)
      lastMessage.set({ source: '', message: '' })
      lastError.set(null)
      cancelAnyInProgressCalls = false

      const storeMessageResponse = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, conversationId }),
      })

      if (!storeMessageResponse.ok) {
        console.error('Error storing message', storeMessageResponse)
        lastError.set(`Error storing message (${storeMessageResponse.status}). Try again or contact support.`)
      }

      const { messageId } = await storeMessageResponse.json()

      const chatUrl = conversationId
        ? `/chat?message=${messageId}&conversation=${conversationId}`
        : `/chat?message=${messageId}&assistant=${assistantId}`

      if (cancelAnyInProgressCalls) {
        return
      }

      es = new EventSource(chatUrl, { withCredentials: true })

      state.set('waiting')

      let accumulatedResponseMessage = ''

      es.onerror = (e) => {
        console.error('chat error', e)
        lastError.set('Error connecting to chat. Try again or contact support.')
        close()
        state.set('error')
      }

      es.addEventListener('chat.conversation_id', (e) => {
        console.log('chat conversation_id', e)
        lastConversationId.set(e.data)
        state.set('responding')
      })

      es.addEventListener('chat.message', (e) => {
        const { source, message } = JSON.parse(e.data)
        accumulatedResponseMessage += message
        console.log('es message', e, accumulatedResponseMessage)
        lastMessage.set({ source, message: accumulatedResponseMessage })
        state.set('responding')
      })

      es.addEventListener('chat.error', (e) => {
        console.error('es message error', e)
        const { message } = JSON.parse(e.data)
        lastError.set(message)
        close()
        state.set('error')
      })

      es.addEventListener('chat.message_end', (e) => {
        console.log('es message end', e)
        close()
      })
    },

    stop: close,
  }
}
