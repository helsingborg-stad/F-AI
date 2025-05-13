import type { RequestEvent } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'

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

export async function replaceContextCollection(
  event: RequestEvent,
  collectionId: string,
  files: File[],
) {
  const formData = new FormData()

  for (const file of files) {
    formData.append('files', file)
  }

  formData.append('urls', '')

  const response = await api.put(`/api/collection/${collectionId}/content`, {
    event,
    body: formData,
  })

  if (response.ok) {
    return await response.json()
  }

  throw new Response('Failed to replace context collection', { status: response.status })
}
