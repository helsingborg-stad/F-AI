import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types.js'
import type { IAssistantModels } from '$lib/types.js'
import { api } from '$lib/api-fetch-factory.js'

export const load: PageServerLoad = async (event) => {
  let models: IAssistantModels[] = []

  const getModelsResponse = await api.get('/api/assistant/models', {
    event,
    withAuth: true,
  })

  if (getModelsResponse.ok) {
    const data = await getModelsResponse.json()
    models = data.models
  }

  return { models }
}

export const actions = {
  create: async (event) => {
    const formData = await event.request.formData()

    const createAssistantResponse = await api.post('/api/assistant', {
      event,
      withAuth: true,
    })

    if (!createAssistantResponse.ok) {
      return { success: false }
    }

    const assistantId = (await createAssistantResponse.json()).assistant_id
    const name = formData.get('name')
    const model = formData.get('model')
    const modelKey = formData.get('model_key')
    const instructions = formData.get('instructions')
    const description = formData.get('description')

    const body = {
      name: name,
      model: model,
      model_key: modelKey,
      instructions: instructions,
      description: description,
    }

    const updateModelResponse = await api.put(`/api/assistant/${assistantId}`, {
      event,
      withAuth: true,
      body,
    })

    if (!updateModelResponse.ok) {
      return { success: false }
    }

    redirect(303, '/assistant')
  },
}
