import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import { getAssistantPickerData } from './utils.js'
import { userCanChat } from '$lib/utils/scopes.js'

export const load: LayoutServerLoad = async (event) => {
  const canChat = await userCanChat(event)

  const assistants = await getAssistantPickerData(event)

  const conversationsResponse = await api.get('/api/conversation', { event })
  if (!conversationsResponse.ok) {
    redirect(307, '/chat')
  }

  const {
    conversations,
  }: {
    conversations: {
      id: string
      timestamp: string
      title: string
    }[]
  } = await conversationsResponse.json()

  if (event.params.conversationId) {
    const response = await api.get(`/api/conversation/${event.params.conversationId}`, {
      event,
    })

    if (!response.ok) {
      redirect(307, '/chat')
    }

    const {
      conversation,
    }: {
      conversation: {
        assistant_id: string
        messages: {
          timestamp: string
          role: string
          content: string
          reasoning: string
        }[]
      }
    } = await response.json()

    const messages = conversation.messages
      .filter((msg) => msg.role != 'system')
      .map((msg) => ({
        timestamp: msg.timestamp,
        source: msg.role,
        message: msg.content,
        reasoning: ''
      }))

    const conversationContext = {
      assistantId: conversation.assistant_id,
      messages: messages,
    }

    return {
      conversationContext,
      assistants,
      conversations,
      canChat: canChat,
    }
  }

  return {
    conversationContext: { assistantId: '', messages: [] },
    assistants,
    conversations,
    canChat: canChat,
  }
}
