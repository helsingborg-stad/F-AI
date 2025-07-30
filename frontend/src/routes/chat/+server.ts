import { error, json } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import type { RequestHandler } from './$types.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

/** Store Message handler */
export const POST: RequestHandler = async (event) => {
  const { message }: { message: string } = await event.request.json()

  const response = await api.post('/api/chat/store',
    {
      body: { message },
      event,
    },
  )

  if (!response.ok) {
    error(response.status, await response.text())
  }

  const { stored_message_id } = await response.json()

  return json({ messageId: stored_message_id })
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
    features
  })
}
