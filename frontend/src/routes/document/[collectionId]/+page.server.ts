import type { PageServerLoad } from './$types.js'
import { userCanReadCollections } from '$lib/utils/scopes.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'
import { type Actions, error } from '@sveltejs/kit'

export const load: PageServerLoad = async (event) => {
  const canView = await userCanReadCollections(event)

  if (canView) {
    const api = new BackendApiServiceFactory().get(event)
    const [apiError, result] = await api.getCollections()

    if (apiError) {
      error(500, apiError)
    }

    const collection = result.find((c) => c.id === event.params.collectionId)

    if (collection) {
      return { collection }
    }
  }

  error(404, 'not found')
}

export const actions: Actions = {
  changeLabel: async (event) => {
    const formData = await event.request.formData()
    const newLabel = formData.get('label')
    const collectionId = event.params.collectionId

    if (!collectionId) {
      error(400, 'bad id')
    }

    if (!newLabel || typeof newLabel !== 'string' || newLabel.length == 0) {
      error(400, 'bad label')
    }

    const api = new BackendApiServiceFactory().get(event)
    const [apiError] = await api.updateCollectionMeta(collectionId, newLabel)

    if (apiError) {
      error(500, apiError)
    }

    return {}
  },

  changeDocuments: async (event) => {
    const formData = await event.request.formData()
    const files = formData.getAll('files') as File[]

    const collectionId = event.params.collectionId

    if (!collectionId) {
      error(400, 'bad id')
    }

    const api = new BackendApiServiceFactory().get(event)
    const [apiError] = await api.updateCollection(collectionId, files)

    if (apiError) {
      error(500, apiError)
    }

    return {}
  },
}
