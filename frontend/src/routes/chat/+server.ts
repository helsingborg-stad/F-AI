import { error, json } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import type { RequestHandler } from './$types.js'

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
  const withWebSearch = event.url.searchParams.get('withWebSearch')

  if (!messageId) {
    error(400, 'message parameter is required')
  }

  if (!conversationId && !assistantId) {
    error(400, 'conversation or assistant parameter is required')
  }

  const url = conversationId
    ? `/api/chat/sse/${conversationId}?stored_message_id=${messageId}&with_web_search=${withWebSearch}`
    : `/api/chat/sse?assistant_id=${assistantId}&stored_message_id=${messageId}&with_web_search=${withWebSearch}`

  return api.get(url, { withAuth: true, event })
}
