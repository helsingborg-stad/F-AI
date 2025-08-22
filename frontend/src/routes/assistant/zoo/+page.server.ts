import { m } from '$lib/paraglide/messages.js'
import type { PageServerLoad } from '../../../../.svelte-kit/types/src/routes/$types.js'
import type { IAssistantCard } from '$lib/types.js'
import {
  addFavoriteAssistant,
  deleteFavoriteAssistant,
  fetchAllAssistants,
  getFavoriteAssistants,
} from '$lib/utils/assistant.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import { userCanReadAssistants } from '$lib/utils/scopes.js'
import { getAvatarProcessor } from '$lib/utils/image/factory.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = await userCanReadAssistants(event)

  let assistantCards: IAssistantCard[] = []

  if (userCanListAssistants) {
    const allAssistants = await fetchAllAssistants(event)

    let favoriteAssistantsMap = new Map()
    const favoriteAssistants = await getFavoriteAssistants(event)
    favoriteAssistantsMap = new Map(
      favoriteAssistants.map((fav: { id: string }) => [fav.id, fav]),
    )

    assistantCards = await Promise.all(
      allAssistants.map(async (assistant) => {
        const avatarProcessor = await getAvatarProcessor()
        const processedAvatar = await avatarProcessor.process(
          assistant.id,
          assistant.meta.avatar_base64 as string | undefined,
        )

        return {
          id: assistant.id,
          avatarThumbnail: processedAvatar.avatarThumbnail,
          avatar: '',
          title: assistant.meta.name?.toString() ?? '',
          description: assistant.meta.description?.toString() ?? '',
          owner: 'Helsingborg',
          starters: (assistant.meta.sample_questions as string[]) ?? [],
          isFavorite: favoriteAssistantsMap.has(assistant.id),
          primaryColor: (assistant.meta.primary_color as string) ?? 'transparent',
          metadata: {
            category: 'Demo',
            conversationCount: '<100',
            likes: '0',
          },
        }
      }),
    )
  }

  const favExhibit = {
    title: m.assistant_zoo_exhibit_favorites_title(),
    description: m.assistant_zoo_exhibit_favorites_description(),
    cards: assistantCards.filter((card) => card.isFavorite),
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
        await addFavoriteAssistant(itemId, event)
      } else {
        await deleteFavoriteAssistant(itemId, event)
      }

      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },
}
