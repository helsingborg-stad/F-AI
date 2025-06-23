import type { IAssistantMenu, IBackendAssistant } from '$lib/types.ts'
import { fetchAllAssistants, getAssistantFavs } from '$lib/utils/assistant.js'
import type { RequestEvent } from '@sveltejs/kit'

export async function getAssistantPickerData(
  event: RequestEvent,
): Promise<IAssistantMenu[]> {
  let result: IAssistantMenu[] = []

  const favAssistantResponse = await getAssistantFavs(event)
  if (!favAssistantResponse.ok) {
    throw new Error(`Failed to get fav assistant`)
  }

  const favAssistantData = await favAssistantResponse.json()
  const favIds = new Set(
    favAssistantData.assistants.map((assistant: IBackendAssistant) => assistant.id),
  )

  if (favAssistantData.assistants.length > 0) {
    const favItems = favAssistantData.assistants.map((assistant: IBackendAssistant) => ({
      id: assistant.id,
      name: assistant.meta.name?.toString() ?? '<unknown>',
      allowSearch: false
    }))

    result = [
      {
        menuTitle: 'Favorites',
        menuItems: favItems,
      },
    ]
  }

  const allAssistantsData = await fetchAllAssistants(event)
  const vanillaAssistants = allAssistantsData.filter((assistant) =>
    assistant.meta.name?.toString().toLowerCase().includes('vanilla'),
  )

  const vanillaItems = vanillaAssistants
    .filter((assistant: IBackendAssistant) => !favIds.has(assistant.id))
    .map((assistant: IBackendAssistant) => ({
      id: assistant.id,
      name: assistant.meta.name?.toString() ?? '<unknown>',
      allowSearch: true
    }))

  if (vanillaItems.length > 0) {
    result.push({
      menuTitle: 'Vanilla assistants',
      menuItems: vanillaItems,
    })
  }

  return result
}
