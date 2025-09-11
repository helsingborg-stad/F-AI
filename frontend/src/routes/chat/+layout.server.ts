import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types.js'
import { getAssistantPickerData } from './utils.js'
import { userCanChat } from '$lib/utils/scopes.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'
import type { IFrontendConversationContext } from '$lib/types.js'

export const load: LayoutServerLoad = async (event) => {
  const api = new BackendApiServiceFactory().get(event)
  const canChat = await userCanChat(event)

  const assistants = await getAssistantPickerData(event)

  const [error, conversations] = await api.getConversations()
  if (error) {
    redirect(307, '/chat')
  }

  if (event.params.conversationId) {
    const [error, conversation] = await api.getConversation(event.params.conversationId)

    if (error) {
      redirect(307, '/chat')
    }

    const messages = conversation.messages
      .filter((msg) => msg.role != 'system')
      .map((msg) => ({
        timestamp: msg.timestamp,
        source: msg.role,
        message: msg.content,
        reasoning: '',
      }))

    const conversationContext: IFrontendConversationContext = {
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
