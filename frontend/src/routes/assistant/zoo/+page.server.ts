import type { PageServerLoad } from '../../../../.svelte-kit/types/src/routes/$types.js'
import { canReadAssistants } from '$lib/state/user.svelte.js'
import type { IAssistantCard } from '$lib/types.js'
import {
  addAssistantFav,
  deleteAssistantFav,
  fetchAllAssistants,
  getAssistantFavs,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()

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
    title: 'Favorite assistants',
    description: 'Only assistants you faved. The best of the best!',
    cards: assistantCards.filter(card => card.isFavorite)
  }

  const hbgExhibit = {
    title: 'Hbg Assistants',
    description: 'Assistant created and shared by your colleagues',
    cards: assistantCards.filter((card) => !card.title.toLowerCase().includes('vanilla')),
  }

  const vanillaExhibit = {
    title: 'Vanilla Assistants',
    description: 'When you don\'t need anything extra',
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