import type { PageServerLoad } from '../../../../.svelte-kit/types/src/routes/$types.js'
import { canReadAssistants } from '$lib/state/user.svelte.js'
import type { IAssistantCard } from '$lib/types.js'
import {
  addAssistantFav,
  deleteAssistantFav,
  fetchAllAssistants, getAssistantFavs,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()

  let assistantCards: IAssistantCard[] = []

  if (userCanListAssistants) {
    // Fetch all assistants
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
      avatar: `data:image/png;base64, ${assistant.avatar_base64}`,
      title: assistant.name,
      description: assistant.description,
      owner: 'Helsingborg',
      starters: assistant.sample_questions,
      isFavorite: favoriteAssistantsMap.has(assistant.id),
      metadata: {
        category: 'Demo',
        conversationCount: '<100',
        likes: '0',
      },
    }))
  }

  const featuredExhibit = {
    title: 'Featured Assistants',
    description: 'Our most popular AI assistants',
    cards: assistantCards.filter((card) => {
      return (
        card.title.toLowerCase().includes('code') ||
        card.title.toLowerCase().includes('writing')
      )
    }),
  }

  const mathExhibit = {
    title: 'Specialized Tools',
    description: 'Domain-specific assistants',
    cards: assistantCards.filter((card) => card.title.toLowerCase().includes('math')),
  }

  const vanillaExhibit = {
    title: 'Vanilla Assistants',
    description: "When you don't need anything extra",
    cards: assistantCards.filter((card) => card.title.toLowerCase().includes('vanilla')),
  }

  return {
    exhibits: [featuredExhibit, mathExhibit, vanillaExhibit],
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
