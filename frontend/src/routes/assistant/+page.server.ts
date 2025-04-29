import type { PageServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import type { IAssistant } from '$lib/types.js'
import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'
import { redirect } from '@sveltejs/kit'

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
    (assistant) => assistant.id === activeAssistantID
  )

  return { assistants, canCreateAssistant: userCanCreateAssistant, activeAssistant, canEditActiveAssistant: userCanEditAssistant }
}

export const actions = {
  create: async (event) => {
    const formData = await event.request.formData()

    const createAssistantResponse = await api.post('/api/assistant', {
      event
    })

    console.log(createAssistantResponse)
    if (!createAssistantResponse.ok) {
      return { success: false }
    }

    const assistantId = (await createAssistantResponse.json()).assistant_id
    redirect(303, `/assistant?assistant_id=${assistantId}`)
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

    throw redirect(303, `/assistant?assistant_id=${assistantId}`)
  }
}