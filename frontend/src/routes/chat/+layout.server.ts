import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'

export const load: LayoutServerLoad = async (event) => {
  const assistantsResponse = await api.get('/api/assistant', { event })

  if (!assistantsResponse.ok) {
    redirect(307, '/chat')
  }

  const { assistants }: {
    assistants: {
      id: string
      name: string
    }[]
  } = await assistantsResponse.json()

  const conversationsResponse = await api.get('/api/conversation', { event })
  if (!conversationsResponse.ok) {
    redirect(307, '/chat')
  }

  const { conversations }: {
    conversations: {
      id: string
      timestamp: string
      title: string
    }[]
  } = await conversationsResponse.json()

  if (event.params.conversationId) {
    const response = await api.get(`/api/conversation/${event.params.conversationId}`, { event })

    if (!response.ok) {
      redirect(307, '/chat')
    }

    const { conversation }: {
      conversation: {
        messages: {
          timestamp: string,
          role: string,
          content: string,
        }[]
      }
    } = await response.json()

    const messages = conversation.messages
      .filter(msg => msg.role != 'system')
      .map(msg => ({
        timestamp: msg.timestamp,
        source: msg.role,
        message: msg.content,
      }))

    return {
      messages,
      assistants,
      conversations,
    }
  }

  return { messages: [], assistants, conversations }
}