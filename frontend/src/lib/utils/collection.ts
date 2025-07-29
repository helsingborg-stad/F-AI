import type { RequestEvent } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import { handleApiCall } from '$lib/utils/handle-api-calls.js'
import type { ICollection } from '$lib/types.js'

export async function createCollection(
  event: RequestEvent,
  body: { label: string; embedding_model: string },
) {
  const response = await api.post('/api/collection', { event, body })

  if (response.ok) {
    return await response.json()
  }

  throw new Response('Failed to create collection', { status: response.status })
}

export async function getCollections(
  event: RequestEvent
): Promise<ICollection[]> {
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
    (api) => api.updateCollection(
      collectionId,
      files
    ),
    'Failed to replace context collection',
    undefined,
  )
}
