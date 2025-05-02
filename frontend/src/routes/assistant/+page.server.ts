import type { PageServerLoad } from './$types.js'
import type { IAssistant } from '$lib/types.js'
import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'
import { error, redirect } from '@sveltejs/kit'
import {
  createAssistant,
  deleteAssistant,
  fetchAllAssistants,
  fetchAssistantById,
  updateAssistant,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'

async function getAssistantFormValues(formData: FormData, overwrite = {}) {
  const modelKey = formData.get('model_key') as string
  const name = formData.get('name') as string
  const model = formData.get('model') as string
  const instructions = formData.get('instructions') as string
  const description = formData.get('description') as string
  const visibility = formData.get('public') === 'on'

  return {
    model_key: modelKey,
    name: name,
    model: model,
    instructions: instructions,
    description: description,
    public: visibility,
    ...overwrite,
  }
}

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()
  const userCanCreateAssistant = canCreateAssistant()
  const userCanEditAssistant = canCreateAssistant()
  const activeAssistantID = event.url.searchParams.get('assistant_id') || ''

  let assistants: IAssistant[] = []
  let activeAssistant: IAssistant = {} as IAssistant

  if (userCanListAssistants) {
    assistants = await fetchAllAssistants(event)
  }

  if (activeAssistantID) {
    activeAssistant = await fetchAssistantById(event, activeAssistantID)
    activeAssistant.id = activeAssistantID
  }

  return {
    assistants,
    activeAssistant,
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

    try {
      const updateData = await getAssistantFormValues(formData)
      await updateAssistant(assistantId, updateData, event)
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
}
