import type { PageServerLoad } from './$types.js'
import { error, redirect } from '@sveltejs/kit'
import { fetchAllAssistants, fetchAssistantById, fetchAssistantModels } from '$lib/utils/assistant.ts'
import type { IAssistant } from '$lib/types.js'
import { api } from '$lib/api-fetch-factory.js'

export const load: PageServerLoad = async (event) => {
  const paramAssistantId = event.url.searchParams.get('assistant_id')
  if (!paramAssistantId) {
    throw error(404, 'Valid assistant ID is required')
  }

  try {
    const [allAssistants, models, queriedAssistant] = await Promise.all([
      fetchAllAssistants(event),
      fetchAssistantModels(event),
      fetchAssistantById(event, paramAssistantId),
    ])

    const matchingAssistant = allAssistants.find(
      (assistant) => assistant.id === paramAssistantId,
    )

    const assistant: IAssistant = {
      ...matchingAssistant,
      ...queriedAssistant,
    }

    return { assistant, models }
  } catch (e) {
    console.error('Error in load function:', e)

    throw error(500, 'Failed to load assistant data')
  }
}

export const actions = {
  delete: async (event) => {
    const formData = await event.request.formData()
    const assistantI = formData.get('assistant_id')

    if (!assistantI) {
      throw error(404, 'Valid assistant ID is required')
    }

    const response = await api.delete(`/api/assistant/${assistantI}`, {
      withAuth: true,
      event,
    })

    if (!response.ok) {
      throw error(500, 'Failed to delete assistant')
    }

    throw redirect(303, '/assistant')
  },

  update: async (event) => {
    const formData = await event.request.formData()
    const assistantId = formData.get('assistant_id')
    const modelKey = formData.get('model_key')
    const name = formData.get('name')
    const model = formData.get('model')
    const instructions = formData.get('instructions')
    const description = formData.get('description')

    const body = {
      model_key: modelKey,
      name: name,
      model: model,
      instructions: instructions,
      description: description,
    }

    await api.put(`/api/assistant/${assistantId}`, {
      event,
      withAuth: true,
      body,
    })

    throw redirect(303, '/assistant')
  },
}
