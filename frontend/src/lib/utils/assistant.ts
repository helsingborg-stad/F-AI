import type { RequestEvent } from '@sveltejs/kit'
import type { IAssistant, IAssistantModels } from '$lib/types.js'
import { api } from '$lib/api-fetch-factory.js'

export async function fetchAllAssistants(event: RequestEvent): Promise<IAssistant[]> {
  const response = await api.get('/api/assistant', { event, withAuth: true })
  if (response.ok) {
    const data = await response.json()
    return data.assistants
  }
  return []
}

export async function fetchAssistantModels(
  event: RequestEvent,
): Promise<IAssistantModels[]> {
  const response = await api.get('/api/assistant/models', { event, withAuth: true })
  if (response.ok) {
    const data = await response.json()
    return data.models
  }
  return []
}

export async function fetchAssistantById(
  event: RequestEvent,
  assistantId: string,
): Promise<IAssistant> {
  const response = await api.get(`/api/assistant/${assistantId}`, {
    event,
    withAuth: true,
  })

  if (response.ok) {
    const data = await response.json()
    if (data.assistant) {
      return data.assistant as IAssistant
    }
  }

  throw new Response('Assistant not found', { status: 404 })
}
