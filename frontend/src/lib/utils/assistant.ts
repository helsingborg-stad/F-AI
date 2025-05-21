import type { RequestEvent } from '@sveltejs/kit'
import type { IAssistant, IAssistantModels, IBackendAssistant } from '$lib/types.js'
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
): Promise<IBackendAssistant> {
  const response = await api.get(`/api/assistant/${assistantId}`, {
    event,
    withAuth: true,
  })

  if (response.ok) {
    const data = await response.json()
    if (data.assistant) {
      return data.assistant as IBackendAssistant
    }
  }

  throw new Response('Assistant not found', { status: 404 })
}

export async function createAssistant(event: RequestEvent): Promise<string> {
  const response = await api.post('/api/assistant', { event, withAuth: true })

  if (!response.ok) {
    throw new Response('Failed to create assistant', { status: response.status })
  }

  const data = await response.json()
  return data.assistant_id
}

export async function updateAssistant(
  assistantId: string,
  updates: {
    name?: string
    description?: string
    model?: string
    instructions?: string
    model_key?: string
    collection_id?: string
  },
  event: RequestEvent,
) {
  const response = await api.put(`/api/assistant/${assistantId}`, {
    event,
    body: updates,
  })

  if (!response.ok) {
    throw new Response('Failed to update assistant', { status: response.status })
  }
}

export async function deleteAssistant(event: RequestEvent, assistantId: string) {
  const response = await api.delete(`/api/assistant/${assistantId}`, {
    event,
  })

  if (!response.ok) {
    throw new Response('Failed to delete assistant', { status: response.status })
  }
}

export async function updateAssistantAvatar(
  assistantId: string,
  avatar: File,
  event: RequestEvent,
) {
  const formData = new FormData()
  formData.append('file', avatar)

  const response = await api.put(`/api/assistant/${assistantId}/avatar`, {
    event,
    body: {
      file: formData
    }
  })

  if (!response.ok) {
    throw new Response('Failed to update assistant avatar', { status: response.status })
  }
}