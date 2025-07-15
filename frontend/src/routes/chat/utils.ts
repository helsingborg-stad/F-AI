import type { RequestEvent } from '@sveltejs/kit'
import { m } from '$lib/paraglide/messages.js'
import type { IAssistantMenu, IBackendAssistant } from '$lib/types.ts'
import { fetchAllAssistants, getAssistantFavs } from '$lib/utils/assistant.js'

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
      name: assistant.meta.name?.toString() ?? m.chat_assistant_picker_name_unknown(),
      allowSearch: Boolean(assistant.meta?.enable_search),
      allowReasoning: Boolean(assistant.meta?.enable_reasoning),
    }))

    result = [
      {
        menuTitle: m.chat_assistant_picker_menu_title_favorites(),
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
      name: assistant.meta.name?.toString() ?? m.chat_assistant_picker_name_unknown(),
      allowSearch: Boolean(assistant.meta?.enable_search),
      allowReasoning: Boolean(assistant.meta?.enable_reasoning),
    }))

  if (vanillaItems.length > 0) {
    result.push({
      menuTitle: m.chat_assistant_picker_menu_title_vanilla(),
      menuItems: vanillaItems,
    })
  }

  return result
}
