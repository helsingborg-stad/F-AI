import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import { canChat } from '$lib/state/user.svelte.js'
import type { JsonObject } from '$lib/types.js'

export const load: LayoutServerLoad = async (event) => {
  const userCanChat = canChat()

  const assistantsResponse = await api.get('/api/assistant', { event })

  if (!assistantsResponse.ok) {
    redirect(307, '/chat')
  }

  const {
    assistants,
  }: {
    assistants: {
      id: string
      meta: JsonObject
    }[]
  } = await assistantsResponse.json()

  const transformedAssistants = assistants.map(a => ({
    id: a.id,
    name: a.meta.name?.toString() ?? '<unknown>',
  }))

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
      assistants: transformedAssistants,
      conversations,
      canChat: userCanChat,
    }
  }

  return {
    conversationContext: { assistantId: '', messages: [] },
    assistants: transformedAssistants,
    conversations,
    canChat: userCanChat,
  }
}
