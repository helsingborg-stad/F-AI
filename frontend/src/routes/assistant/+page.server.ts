import type { PageServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import type { IAssistant } from '$lib/types.js'
import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()
  const userCanCreateAssistant = canCreateAssistant()
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

  return { assistants, canCreateAssistant: userCanCreateAssistant, activeAssistant }
}
