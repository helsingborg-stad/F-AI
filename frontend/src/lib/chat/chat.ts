export interface RealtimeChatMessage {
  source: string,
  message: string,
}

export async function sendChatMessage(
  message: string,
  assistantId: string | undefined,
  conversationId: string | undefined,
  onAddMessage: (message: RealtimeChatMessage) => void,
  onUpdateLastMessage: (message: RealtimeChatMessage) => void,
  onGoto: (url: string) => void,
  onError: (error: string) => void) {

  onAddMessage({ source: 'user', message: message })
  onAddMessage({ source: 'assistant', message: '...' })

  const storeMessageResponse = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversationId }),
  })

  if (!storeMessageResponse.ok) {
    console.error('Error storing message', storeMessageResponse)
    onError(`Error storing message (${storeMessageResponse.status}). Try again or contact support.`)
    return
  }

  const { messageId } = await storeMessageResponse.json()

  let accumulatedResponseMessage = ''

  const chatUrl = conversationId
    ? `/chat?message=${messageId}&conversation=${conversationId}`
    : `/chat?message=${messageId}&assistant=${assistantId}`

  const es = new EventSource(chatUrl, { withCredentials: true })
  es.onerror = (e) => {
    console.error('chat error', e)
    onError('Error connecting to chat. Try again or contact support.')
    es.close()
  }
  es.addEventListener('chat.conversation_id', (e) => {
    console.log('chat conversation_id', e)
    conversationId = e.data
    onGoto(`/chat/${e.data}`)
  })
  es.addEventListener('chat.message', (e) => {
    const { source, message } = JSON.parse(e.data)
    accumulatedResponseMessage += message
    console.log('es message', e, accumulatedResponseMessage)
    onUpdateLastMessage({ source, message: accumulatedResponseMessage })
  })
  es.addEventListener('chat.error', (e) => {
    console.error('es message error', e)
    const { message } = JSON.parse(e.data)
    onError(message)
    es.close()
  })
  es.addEventListener('chat.message_end', (e) => {
    console.log('es message end', e)
    es.close()
  })
}