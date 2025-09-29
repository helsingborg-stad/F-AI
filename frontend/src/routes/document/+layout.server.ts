import { error, type RequestEvent } from '@sveltejs/kit'
import { userCanReadCollections, userCanWriteCollections } from '$lib/utils/scopes.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'
import type { ICollection } from '$lib/types.js'

export async function load(event: RequestEvent) {
  const canView = await userCanReadCollections(event)
  const canEdit = await userCanWriteCollections(event)

  let collections: ICollection[] = []

  if (canView) {
    const api = new BackendApiServiceFactory().get(event)
    const [apiError, result] = await api.getCollections()
    if (apiError !== null) {
      error(500, apiError)
    }
    collections = result || []
  }

  console.log('layout reload')

  return {
    canView,
    canEdit,
    collections: collections.reverse(), // TODO: should add createdAt/modifiedAt and sort instead
  }
}
