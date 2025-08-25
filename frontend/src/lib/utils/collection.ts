import type { RequestEvent } from '@sveltejs/kit'
import { handleApiCall } from '$lib/utils/handle-api-calls.js'
import type { ICollection } from '$lib/types.js'

export async function createCollection(
  event: RequestEvent,
  label: string,
  embeddingModel: string,
) {
  return handleApiCall(
    event,
    (api) => api.createCollection(label, embeddingModel),
    'Failed to create collection',
    '',
  )
}

export async function getCollections(event: RequestEvent): Promise<ICollection[]> {
  return handleApiCall(
    event,
    (api) => api.getCollections(),
    'Failed to get collections',
    [],
  )
}

export async function replaceContextCollection(
  event: RequestEvent,
  collectionId: string,
  files: File[],
) {
  return handleApiCall(
    event,
    (api) => api.updateCollection(collectionId, files),
    'Failed to replace context collection',
    undefined,
  )
}
