import { error, json } from '@sveltejs/kit'
import type { RequestHandler } from './$types.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

/** Store Message handler */
export const POST: RequestHandler = async (event) => {
  const { message }: { message: string } = await event.request.json()
  const apiServiceFactory = new BackendApiServiceFactory()
  const apiService = apiServiceFactory.get(event)

  const [err, messageId] = await apiService.storeChatSSE(message)

  if (err) {
    error(500, err)
  }

  return json({ messageId })
}

/** SSE chat handler */
export const GET: RequestHandler = async (event) => {
  const messageId = event.url.searchParams.get('message')
  const conversationId = event.url.searchParams.get('conversation')
  const assistantId = event.url.searchParams.get('assistant')
  const features = event.url.searchParams.get('features') ?? ''
  const apiServiceFactory = new BackendApiServiceFactory()

  if (!messageId) {
    error(400, 'message parameter is required')
  }

  if (!conversationId && !assistantId) {
    error(400, 'conversation or assistant parameter is required')
  }

  const apiService = apiServiceFactory.get(event)

  return apiService.getChatSSE({
    messageId,
    conversationId: conversationId || undefined,
    assistantId: assistantId || undefined,
    features,
  })
}
