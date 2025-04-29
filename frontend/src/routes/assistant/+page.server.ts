import type { PageServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import type { IAssistant } from '$lib/types.js'
import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'
import { error, redirect } from '@sveltejs/kit'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()
  const userCanCreateAssistant = canCreateAssistant()
  const userCanEditAssistant = true
  const activeAssistantID = event.url.searchParams.get('assistant_id') || ''

  let assistants: IAssistant[] = []

  if (userCanListAssistants) {
    const response = await api.get('/api/assistant', { event, withAuth: true })

    if (response.ok) {
      const data = await response.json()
      assistants = data.assistants
    }
  }

  const activeAssistant = assistants.find(
    (assistant) => assistant.id === activeAssistantID,
  )

  return {
    assistants,
    canCreateAssistant: userCanCreateAssistant,
    activeAssistant,
    canEditActiveAssistant: userCanEditAssistant,
  }
}

async function createAssistant(event) {
  const response = await api.post('/api/assistant', {
    event,
  })

  if (!response.ok) {
    return { success: false, assistantId: null }
  }

  const assistantId = (await response.json()).assistant_id
  return { success: true, assistantId }
}

async function updateAssistant(event, assistantId = null) {
  const formData = await event.request.formData()
  const computedAssistantId = assistantId ? assistantId : formData.get('assistant_id')
  const modelKey = formData.get('model_key')
  const name = formData.get('name')
  const model = formData.get('model')
  const instructions = formData.get('instructions')
  const description = formData.get('description')

  const body = {
    model_key: modelKey,
    name: assistantId ? `Copy of ${name}` : name,
    model: model,
    instructions: instructions,
    description: description,
  }

  const response = await api.put(`/api/assistant/${computedAssistantId}`, {
    event,
    body,
  })

  if (!response.ok) {
    return { success: false, assistantId: null }
  }

  return { success: true, assistantId: computedAssistantId }
}

export const actions = {
  create: async (event) => {
    const { success, assistantId } = await createAssistant(event)

    if (!success) {
      return { success: false }
    }

    redirect(303, `/assistant?assistant_id=${assistantId}`)
  },

  update: async (event) => {
    const { success, assistantId } = await updateAssistant(event)

    if (!success) {
      return { success: false }
    }

    throw redirect(303, `/assistant?assistant_id=${assistantId}`)
  },

  delete: async (event) => {
    const formData = await event.request.formData()
    const assistantI = formData.get('assistant_id')

    if (!assistantI) {
      throw error(404, 'Valid assistant ID is required')
    }

    const response = await api.delete(`/api/assistant/${assistantI}`, {
      event,
    })

    if (!response.ok) {
      throw error(500, 'Failed to delete assistant')
    }

    throw redirect(303, '/assistant')
  },

  copy: async (event) => {
    const { success, assistantId } = await createAssistant(event)

    if (!success) {
      return { success: false }
    }

    const { success: updateSuccess } = await updateAssistant(event, assistantId)

    if (!updateSuccess) {
      return { success: false }
    }

    redirect(303, `/assistant?assistant_id=${assistantId}`)
  },
}
