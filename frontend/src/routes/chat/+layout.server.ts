import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'

export const load: LayoutServerLoad = async (event) => {
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
    }
  }

  return { messages: [] }
}