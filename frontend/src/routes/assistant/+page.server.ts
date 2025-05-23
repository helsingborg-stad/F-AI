import type { PageServerLoad } from './$types.js'
import type { IAssistant, IBackendAssistant, ICollection } from '$lib/types.js'
import {
  canCreateAssistant,
  canReadAssistants,
  canReadCollections,
} from '$lib/state/user.svelte.js'
import { error, redirect } from '@sveltejs/kit'
import {
  createAssistant,
  deleteAssistant,
  deleteAssistantAvatar,
  fetchAllAssistants,
  fetchAssistantById,
  fetchAssistantModels,
  updateAssistant,
  updateAssistantAvatar,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import {
  createCollection,
  getCollections,
  replaceContextCollection,
} from '$lib/utils/collection.js'

function getAssistantFormValues(formData: FormData, overwrite = {}): IBackendAssistant {
  const modelKey = formData.get('model_key') as string
  const name = formData.get('name') as string
  const model = formData.get('model') as string
  const collectionId = formData.get('collection_id') as string
  const instructions = formData.get('instructions') as string
  const description = formData.get('description') as string
  const visibility = formData.get('public') === 'on'
  const avatar = formData.get('avatar_base64') as string
  const primaryColor = formData.get('primary_color') as string

  return {
    model_key: modelKey,
    name: name,
    model: model,
    collection_id: collectionId,
    instructions: instructions,
    description: description,
    is_public: visibility,
    avatar_base64: avatar,
    primary_color: primaryColor,
    ...overwrite,
  }
}

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()
  const userCanCreateAssistant = canCreateAssistant()
  const userCanEditAssistant = canCreateAssistant()
  const userCanReadCollections = canReadCollections()
  const activeAssistantID = event.url.searchParams.get('assistant_id') || ''

  let assistants: IAssistant[] = []
  let activeAssistant: IAssistant = {} as IAssistant

  if (userCanListAssistants) {
    assistants = (await fetchAllAssistants(event)).map((assistant) => ({
      id: assistant.id,
      name: assistant.name,
      description: assistant.description,
      instructions: assistant.instructions,
      model: assistant.model,
      isPublic: assistant.is_public,
      avatarBase64: assistant.avatar_base64,
      primaryColor: assistant.primary_color,
    }))
  }

  if (activeAssistantID) {
    const assistantData = await fetchAssistantById(event, activeAssistantID)
    activeAssistant = {
      id: activeAssistantID,
      name: assistantData.name,
      description: assistantData.description,
      instructions: assistantData.instructions,
      model: assistantData.model,
      isPublic: assistantData.is_public,
      avatarBase64: assistantData.avatar_base64,
      primaryColor: assistantData.primary_color,
    }

    if (userCanReadCollections && assistantData.collection_id) {
      try {
        const collections = (await getCollections(event)).collections
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
    canCreateAssistant: userCanCreateAssistant,
    canEditActiveAssistant: userCanEditAssistant,
  }
}

export const actions = {
  create: async (event) => {
    let assistantId = ''

    try {
      assistantId = await createAssistant(event)
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant?assistant_id=${assistantId}`)
  },

  update: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id') as string
    const avatar = formData.get('avatar') as File
    const shouldDeleteAvatar = formData.get('delete_avatar') === 'true'

    try {
      const updateData = await getAssistantFormValues(formData)
      await updateAssistant(assistantId, updateData, event)

      // Only process avatar changes if there's a new file or explicit deletion request
      if (avatar && avatar.size > 0) {
        // User uploaded a new avatar
        await updateAssistantAvatar(assistantId, avatar, event)
      } else if (shouldDeleteAvatar) {
        // User explicitly clicked the delete button
        await deleteAssistantAvatar(assistantId, event)
      }
      // Otherwise, keep the existing avatar unchanged
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant?assistant_id=${assistantId}`)
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

    redirect(303, '/assistant')
  },

  copy: async (event) => {
    const formData = await event.request.formData()
    const originalName = formData.get('name') as string
    let assistantId = ''

    try {
      assistantId = await createAssistant(event)
      const updateData = await getAssistantFormValues(formData, {
        name: `Copy of ${originalName}`,
      })
      await updateAssistant(assistantId, updateData, event)
    } catch (error) {
      return handleApiError(error)
    }

    redirect(303, `/assistant?assistant_id=${assistantId}`)
  },

  uploadFiles: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id') as string
    let collectionId = ''

    try {
      const body = {
        label: 'collection',
        embedding_model: 'default',
      }

      const collectionResponse = await createCollection(event, body)
      collectionId = collectionResponse.collection_id
    } catch (error) {
      return handleApiError(error)
    }

    const files = formData.getAll('files') as File[]
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

    redirect(303, `/assistant?assistant_id=${assistantId}`)
  },
}
