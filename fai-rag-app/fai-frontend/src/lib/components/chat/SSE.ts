export interface ChatMessage {
  id: string
  user: string
  content: string
  timestamp: string
  isSelf: boolean
}

export interface IncomingMessage {
  timestamp: string
  source?: string
  content: string
}

export function incomingMessageToChatMessage(sse: IncomingMessage): ChatMessage {
  return {
    id: sse.timestamp,
    user: sse.source ?? '',
    content: sse.content ?? '',
    timestamp: sse.timestamp,
    isSelf: sse.source == 'user',
  }
}

export class SSE {
  eventSource: EventSource | null = null
  errorCallback: () => void
  updateConversationIdCallback: (id: string) => void
  addOrUpdateMessageCallback: (message: ChatMessage) => void
  onRequestStatusChangedCallback: (isRequestRunning: boolean) => void

  idCounter = 0
  lastMessage: ChatMessage | null = null

  constructor(
    errorCallback,
    updateConversationIdCallback,
    addOrUpdateMessageCallback,
    onRequestStatusChangedCallback,
  ) {
    this.errorCallback = errorCallback
    this.updateConversationIdCallback = updateConversationIdCallback
    this.addOrUpdateMessageCallback = addOrUpdateMessageCallback
    this.onRequestStatusChangedCallback = onRequestStatusChangedCallback
  }

  close() {
    if (this.eventSource !== null) {
      this.eventSource.close()
      this.eventSource = null
    }
    this.onRequestStatusChangedCallback(false)
  }

  create(
    question: string,
    conversationId: string | null,
    assistantProject: string | undefined,
    assistantId: string | undefined,
  ) {
    if (question.length == 0) return

    this.addOrUpdateMessageCallback({
      id: `${++this.idCounter}`,
      isSelf: true,
      user: 'Me',
      content: question,
      timestamp: new Date().toISOString(),
    })

    this.lastMessage = {
      id: `${++this.idCounter}`,
      isSelf: false,
      user: '',
      content: '',
      timestamp: '',
    }

    this.addOrUpdateMessageCallback(this.lastMessage)

    this.close()

    this.onRequestStatusChangedCallback(true)

    fetch('/api/sse/chat/question', {
      method: 'POST',
      body: JSON.stringify({ question }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((response) => {
        const questionId = response.id

        const fullEndpoint = conversationId
          ? `/api/sse/chat/stream/continue/${conversationId}?stored_question_id=${questionId}`
          : `/api/sse/chat/stream/new/${assistantProject}/${assistantId}?stored_question_id=${questionId}`

        this.eventSource = new EventSource(fullEndpoint)

        this.eventSource.onerror = (e) => {
          console.error(e)
          this.errorCallback()
          this.close()
        }

        this.eventSource.addEventListener('message_end', () => {
          this.close()
        })

        this.eventSource.addEventListener('conversation_id', (e) => {
          this.updateConversationIdCallback(e.data)
        })

        this.eventSource.addEventListener('exception', () => {
          this.errorCallback()
        })

        this.eventSource.addEventListener('message', (e) => {
          try {
            const bytes = Uint8Array.from(atob(e.data), (m) => m.codePointAt(0))
            const jsonString = new TextDecoder().decode(bytes)
            const messagePayload = JSON.parse(jsonString) as IncomingMessage
            const chatMessage = incomingMessageToChatMessage(messagePayload)

            this.lastMessage = {
              ...this.lastMessage,
              ...chatMessage,
              id: this.lastMessage!.id,
              content: this.lastMessage?.content + chatMessage.content,
            }

            this.addOrUpdateMessageCallback(this.lastMessage)
          } catch (ex) {
            console.error('Failed to parse raw message', ex, e)
            this.close()
          }
        })
      })
  }
}
