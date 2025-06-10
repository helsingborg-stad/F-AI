import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import { canChat } from '$lib/state/user.svelte.js'
import { getAssistantPickerData } from './utils.js'

export const load: LayoutServerLoad = async (event) => {
  const userCanChat = canChat()

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
        }[]
      }
    } = await response.json()

    const messages = conversation.messages
      .filter((msg) => msg.role != 'system')
      .map((msg) => ({
        timestamp: msg.timestamp,
        source: msg.role,
        message: msg.content,
      }))

    const conversationContext = {
      assistantId: conversation.assistant_id,
      messages: messages,
    }

    return {
      conversationContext,
      assistants,
      conversations,
      canChat: userCanChat,
    }
  }

  return {
    conversationContext: { assistantId: '', messages: [] },
    assistants,
    conversations,
    canChat: userCanChat,
  }
}
