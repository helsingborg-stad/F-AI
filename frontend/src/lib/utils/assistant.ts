import type { RequestEvent } from '@sveltejs/kit'
import type { IAssistantModels, IBackendAssistant } from '$lib/types.js'
import { api } from '$lib/api-fetch-factory.js'
import {
  type ApiResult,
  BackendApiService,
  BackendApiServiceFactory,
} from '$lib/backendApi/backendApi.js'

async function handleApiCall<T>(
  event: RequestEvent,
  apiMethod: (api: BackendApiService) => Promise<ApiResult<T>>,
  errorMessage: string,
  defaultValue: T,
): Promise<T> {
  const api = new BackendApiServiceFactory().get(event)
  const [error, result] = await apiMethod(api)

  if (error) {
    console.error(errorMessage, error)
    return defaultValue
  }

  return result || defaultValue
}

export async function fetchAllAssistants(
  event: RequestEvent,
): Promise<IBackendAssistant[]> {
  return handleApiCall(
    event,
    (api) => api.getAssistants(),
    'Failed to fetch assistants',
    [],
  )
}

export async function getUserAssistants(
  event: RequestEvent,
): Promise<IBackendAssistant[]> {
  return handleApiCall(
    event,
    (api) => api.getMyAssistants(),
    'Failed to fetch assistants',
    [],
  )
}

export async function fetchAssistantModels(
  event: RequestEvent,
): Promise<IAssistantModels[]> {
  return handleApiCall(
    event,
    (api) => api.getAssistantModels(),
    'Failed to fetch assistant models',
    [],
  )
}

export async function fetchAssistantById(
  event: RequestEvent,
  assistantId: string,
): Promise<IBackendAssistant> {
  return handleApiCall(
    event,
    (api) => api.getAssistant(assistantId),
    'Failed to fetch assistant',
    {
      id: '',
      model: '',
      model_key: '',
      instructions: '',
      meta: {},
      collection_id: null,
      max_collection_results: '0',
    },
  )
}

export async function createAssistant(event: RequestEvent): Promise<string> {
  return handleApiCall(
    event,
    (api) => api.createAssistant(),
    'Failed to create assistant',
    '',
  )
}

export async function updateAssistant(
  assistantId: string,
  updates: {
    name?: string
    description?: string
    model?: string
    instructions?: string
    model_key?: string
    collection_id?: string | null
    max_collection_results?: string
  },
  event: RequestEvent,
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.updateAssistant(assistantId, updates),
    'Failed to update assistant',
    undefined,
  )
}

export async function deleteAssistant(
  event: RequestEvent,
  assistantId: string,
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.deleteAssistant(assistantId),
    'Failed to delete assistant',
    undefined,
  )
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
    body: formData,
  })

  if (!response.ok) {
    throw new Response('Failed to update assistant avatar', { status: response.status })
  }
}

export async function deleteAssistantAvatar(assistantId: string, event: RequestEvent) {
  const response = await api.delete(`/api/assistant/${assistantId}/avatar`, {
    event,
  })

  if (!response.ok) {
    throw new Response('Failed to delete assistant avatar', { status: response.status })
  }
}

export async function addAssistantFav(assistantId: string, event: RequestEvent) {
  const response = await api.post(`/api/assistant/me/favorite/${assistantId}`, { event })

  if (!response.ok) {
    throw new Response('Failed to favorite assistant', { status: response.status })
  }
}

export async function deleteAssistantFav(assistantId: string, event: RequestEvent) {
  const response = await api.delete(`/api/assistant/me/favorite/${assistantId}`, {
    event,
  })

  if (!response.ok) {
    throw new Response('Failed to favorite assistant', { status: response.status })
  }
}

export async function getAssistantFavs(event: RequestEvent) {
  const response = await api.get('/api/assistant/me/favorite', { event })

  if (!response.ok) {
    throw new Response('Failed to fetch favorite assistants', { status: response.status })
  }

  return response
}
