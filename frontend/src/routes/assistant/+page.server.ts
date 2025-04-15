import type { PageServerLoad } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import type { IAssistants } from '$lib/types.js'

export const load: PageServerLoad = async (event) => {
  let assistants: IAssistants[] = []

  const response = await api.get('/api/assistant', { event, withAuth: true })

  if (response.ok) {
    const data = await response.json()
    assistants = data.assistants
  }

  return { assistants }
}
