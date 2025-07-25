import { m } from '$lib/paraglide/messages.js'
import type { PageServerLoad } from '../../../../.svelte-kit/types/src/routes/$types.js'
import type { IAssistantCard } from '$lib/types.js'
import {
  addAssistantFav,
  deleteAssistantFav,
  fetchAllAssistants,
  getAssistantFavs,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import { userCanReadAssistants } from '$lib/utils/scopes.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = await userCanReadAssistants(event)

  let assistantCards: IAssistantCard[] = []

  if (userCanListAssistants) {
    const allAssistants = await fetchAllAssistants(event)

    let favoriteAssistantsMap = new Map()
    try {
      const favoriteResponse = await getAssistantFavs(event)

      if (favoriteResponse.ok) {
        const favoriteData = await favoriteResponse.json()

        favoriteAssistantsMap = new Map(
          favoriteData.assistants.map((fav: { id: string }) => [fav.id, fav]),
        )
      }
    } catch (error) {
      console.error('Failed to fetch favorite assistants:', error)
    }

    assistantCards = allAssistants.map((assistant) => ({
      id: assistant.id,
      avatar: assistant.meta.avatar_base64 ? `data:image/png;base64, ${assistant.meta.avatar_base64}` : null,
      title: assistant.meta.name?.toString() ?? '',
      description: assistant.meta.description?.toString() ?? '',
      owner: 'Helsingborg',
      starters: assistant.meta.sample_questions as string[] ?? [],
      isFavorite: favoriteAssistantsMap.has(assistant.id),
      primaryColor: assistant.meta.primary_color as string ?? 'transparent',
      metadata: {
        category: 'Demo',
        conversationCount: '<100',
        likes: '0',
      },
    }))
  }

  const favExhibit = {
    title: m.assistant_zoo_exhibit_favorites_title(),
    description: m.assistant_zoo_exhibit_favorites_description(),
    cards: assistantCards.filter(card => card.isFavorite)
  }

  const hbgExhibit = {
    title: m.assistant_zoo_exhibit_hbg_title(),
    description: m.assistant_zoo_exhibit_hbg_description(),
    cards: assistantCards.filter((card) => !card.title.toLowerCase().includes('vanilla')),
  }

  const vanillaExhibit = {
    title: m.assistant_zoo_exhibit_vanilla_title(),
    description: m.assistant_zoo_exhibit_vanilla_description(),
    cards: assistantCards.filter((card) => card.title.toLowerCase().includes('vanilla')),
  }

  return {
    exhibits: [favExhibit, hbgExhibit, vanillaExhibit],
  }
}

export const actions = {
  toggleFavorite: async (event) => {
    const data = await event.request.formData()
    const itemId = data.get('itemId') as string
    const isFavorite = data.get('isFavorite') === 'on'

    try {
      if (isFavorite) {
        await addAssistantFav(itemId, event)
      } else {
        await deleteAssistantFav(itemId, event)
      }

      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },
}
