import type { PageServerLoad } from './$types.js'
import type { IAssistant, IBackendAssistant, ICollection } from '$lib/types.js'
import { error, redirect } from '@sveltejs/kit'
import {
  addAssistantFav,
  createAssistant,
  deleteAssistant,
  deleteAssistantAvatar,
  fetchAssistantById,
  fetchAssistantModels,
  getUserAssistants,
  updateAssistant,
  updateAssistantAvatar,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import {
  createCollection,
  getCollections,
  replaceContextCollection,
} from '$lib/utils/collection.js'
import {
  userCanReadAssistants,
  userCanReadCollections,
  userCanWriteAssistant,
} from '$lib/utils/scopes.js'

function getAssistantFormValues(formData: FormData, overwrite = {}): IBackendAssistant {
  const id = formData.get('assistant_id') as string
  const modelKey = formData.get('model_key') as string
  const name = formData.get('name') as string
  const model = formData.get('model') as string
  const collectionId = formData.get('collection_id') as string
  const instructions = formData.get('instructions') as string
  const description = formData.get('description') as string
  const visibility = formData.get('public') === 'on'
  const avatar = formData.get('avatar_base64') as string
  const primaryColor = formData.get('primary_color') as string
  const maxCollectionResults = formData.get('max_collection_results') as string
  const enableSearch = formData.get('enable_search') === 'true'
  const enableReasoning = formData.get('enable_reasoning') === 'true'

  return {
    id: id,
    model_key: modelKey,
    meta: {
      name: name,
      description: description,
      is_public: visibility,
      avatar_base64: avatar,
      primary_color: primaryColor,
      sample_questions: [],
      enable_search: enableSearch,
      enable_reasoning: enableReasoning,
    },
    model: model,
    collection_id: collectionId === '' ? null : collectionId,
    instructions: instructions,
    max_collection_results: maxCollectionResults,
    ...overwrite,
  }
}

export const load: PageServerLoad = async (event) => {
  const canListAssistants = await userCanReadAssistants(event)
  const canCreateAssistant = await userCanWriteAssistant(event)
  const canEditAssistant = await userCanWriteAssistant(event)
  const canReadCollections = await userCanReadCollections(event)
  const activeAssistantID = event.url.searchParams.get('assistant_id') || ''

  let assistants: IAssistant[] = []
  let activeAssistant: IAssistant = {} as IAssistant

  if (canListAssistants) {
    assistants = (await getUserAssistants(event)).map((assistant) => ({
      id: assistant.id,
      name: assistant.meta?.name?.toString() ?? '',
      description: assistant.meta?.description?.toString() ?? '',
      instructions: assistant.instructions,
      model: assistant.model,
      maxCollectionResults: assistant.max_collection_results,
      isPublic: assistant.meta.is_public === true,
      avatarBase64: assistant.meta?.avatar_base64?.toString() ?? '',
      primaryColor: assistant.meta?.primary_color?.toString() ?? '#ffffff',
      enableSearch: assistant.meta?.enable_search === true,
      enableReasoning: assistant.meta?.enable_reasoning === true,
    }))
  }

  if (activeAssistantID) {
    const assistantData = await fetchAssistantById(event, activeAssistantID)
    activeAssistant = {
      id: activeAssistantID,
      name: assistantData.meta?.name?.toString() ?? '',
      description: assistantData.meta?.description?.toString() ?? '',
      instructions: assistantData.instructions,
      model: assistantData.model,
      maxCollectionResults: assistantData.max_collection_results,
      isPublic: assistantData.meta.is_public === true,
      avatarBase64: assistantData.meta?.avatar_base64?.toString() ?? '',
      primaryColor: assistantData.meta?.primary_color?.toString() ?? '#ffffff',
      enableSearch: assistantData.meta?.enable_search === true,
      enableReasoning: assistantData.meta?.enable_reasoning === true,
    }

    if (canReadCollections && assistantData.collection_id) {
      try {
        const collections: ICollection[] = await getCollections(event)
        activeAssistant.collection = collections.find(
          (c: ICollection) => c.id === assistantData.collection_id,
        )
      } catch (error) {
        return handleApiError(error)
      }
    }
  }

  const models = await fetchAssistantModels(event)

  return {
    assistants,
    activeAssistant,
    models,
    canCreateAssistant: canCreateAssistant,
    canEditActiveAssistant: canEditAssistant,
  }
}

export const actions = {
  create: async (event) => {
    let assistantId = ''

    try {
      assistantId = await createAssistant(event)
      await addAssistantFav(assistantId, event)
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant/edit/?assistant_id=${assistantId}`)
  },

  update: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id') as string
    const avatar = formData.get('avatar') as File
    const shouldDeleteAvatar = formData.get('delete_avatar') === 'true'

    try {
      const updateData = getAssistantFormValues(formData)
      await updateAssistant(assistantId, updateData, event)

      if (avatar && avatar.size > 0) {
        await updateAssistantAvatar(assistantId, avatar, event)
      } else if (shouldDeleteAvatar) {
        await deleteAssistantAvatar(assistantId, event)
      }
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant/edit/?assistant_id=${assistantId}`)
  },

  delete: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id') as string

    if (!assistantId) {
      throw error(404, 'Valid assistant ID is required')
    }

    try {
      await deleteAssistant(event, assistantId)
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, '/assistant/edit')
  },

  copy: async (event) => {
    const formData = await event.request.formData()
    const originalName = formData.get('name') as string
    let assistantId = ''

    try {
      assistantId = await createAssistant(event)
      const updateData = getAssistantFormValues(formData, {
        name: `Copy of ${originalName}`,
      })
      await updateAssistant(assistantId, updateData, event)
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant/edit?assistant_id=${assistantId}`)
  },

  uploadFiles: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id') as string
    const files = formData.getAll('files') as File[]
    const label = (formData.get('collection') as string) || 'collection'
    const embeddingModel = (formData.get('embedding_model') as string) || 'default'
    const urls = ['']
    let collectionId = ''

    try {
      collectionId = await createCollection(event, label, embeddingModel)
    } catch (error) {
      return handleApiError(error)
    }

    try {
      await replaceContextCollection(event, collectionId, files)
    } catch (error) {
      return handleApiError(error)
    }

    try {
      const updateData = { collection_id: collectionId }
      await updateAssistant(assistantId, updateData, event)
    } catch (error) {
      return handleApiError(error)
    }

    const fileMetadata = files.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type,
    }))

    const collection: ICollection = {
      id: collectionId,
      label: label,
      files: fileMetadata,
      urls: urls,
      embedding_model: embeddingModel,
    }

    return {
      collection,
    }
  },
}
