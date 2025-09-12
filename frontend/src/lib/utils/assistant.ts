import type { RequestEvent } from '@sveltejs/kit'
import type { IAssistantModel, IBackendAssistant, IFavAssistant } from '$lib/types.js'
import { handleApiCall } from '$lib/utils/handle-api-calls.js'
import type { ApiResult } from '$lib/backendApi/backendApi.js'

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
): Promise<IAssistantModel[]> {
  return handleApiCall(
    event,
    (api) => api.getAllModels(),
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
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.updateAssistantAvatar(assistantId, avatar),
    'Failed to update assistant avatar',
    undefined,
  )
}

export async function deleteAssistantAvatar(
  assistantId: string,
  event: RequestEvent,
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.deleteAssistantAvatar(assistantId),
    'Failed to delete assistant avatar',
    undefined,
  )
}

export async function addFavoriteAssistant(
  assistantId: string,
  event: RequestEvent,
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.addFavoriteAssistant(assistantId),
    'Failed to favorite assistant',
    undefined,
  )
}

export async function deleteFavoriteAssistant(
  assistantId: string,
  event: RequestEvent,
): Promise<void> {
  await handleApiCall(
    event,
    (api) => api.deleteFavoriteAssistant(assistantId),
    'Failed to unfavorite assistant',
    undefined,
  )
}

export async function getFavoriteAssistants(
  event: RequestEvent,
): Promise<IFavAssistant[]> {
  return await handleApiCall(
    event,
    (api) => api.getFavoriteAssistants(),
    'Failed to fetch favorite assistants',
    [],
  )
}
