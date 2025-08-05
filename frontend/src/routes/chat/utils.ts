import type { RequestEvent } from '@sveltejs/kit'
import { m } from '$lib/paraglide/messages.js'
import type { IAssistantMenu, IBackendAssistant } from '$lib/types.ts'
import { fetchAllAssistants, getFavoriteAssistants } from '$lib/utils/assistant.js'
import { createAssistantMenu } from '$lib/type-factory.js'

export async function getAssistantPickerData(
  event: RequestEvent,
): Promise<IAssistantMenu[]> {
  let result: IAssistantMenu[] = []

  const favAssistants = await getFavoriteAssistants(event)
  const favIds = new Set(
    favAssistants.map((assistant) => assistant.id),
  )

  if (favAssistants.length > 0) {
    const favItems = favAssistants.map((assistant) => ({
      id: assistant.id,
      name: assistant.meta.name?.toString() ?? m.chat_assistant_picker_name_unknown(),
      allowSearch: Boolean(assistant.meta?.enable_search),
      allowReasoning: Boolean(assistant.meta?.enable_reasoning),
    }))

    result = [
      createAssistantMenu({
        menuTitle: m.chat_assistant_picker_menu_title_favorites(),
        menuItems: favItems,
      }),
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
    result.push(
      createAssistantMenu({
        menuTitle: m.chat_assistant_picker_menu_title_vanilla(),
        menuItems: vanillaItems,
      }),
    )
  }

  const generalAssistants = allAssistantsData.filter(
    (assistant) => !vanillaAssistants.includes(assistant),
  )
  const moreItems = generalAssistants.map((assistant: IBackendAssistant) => ({
    id: assistant.id,
    name: assistant.meta.name?.toString() ?? m.chat_assistant_picker_name_unknown(),
    allowSearch: Boolean(assistant.meta?.enable_search),
    allowReasoning: Boolean(assistant.meta?.enable_reasoning),
  }))

  if (moreItems.length > 0) {
    result.push(
      createAssistantMenu({
        menuTitle: m.chat_assistant_picker_menu_title_general(),
        hidden: true,
        menuItems: moreItems,
      }),
    )
  }

  return result
}
