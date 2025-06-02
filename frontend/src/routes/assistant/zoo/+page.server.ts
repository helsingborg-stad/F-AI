import type { PageServerLoad } from '../../../../.svelte-kit/types/src/routes/$types.js'
import { canReadAssistants } from '$lib/state/user.svelte.js'
import type { IAssistantCard } from '$lib/types.js'
import { fetchAllAssistants } from '$lib/utils/assistant.js'

export const load: PageServerLoad = async (event) => {
  const userCanListAssistants = canReadAssistants()

  let assistantCards: IAssistantCard[] = []

  if (userCanListAssistants) {
    assistantCards = (await fetchAllAssistants(event)).map((assistant) => ({
      id: assistant.id,
      avatar: `data:image/png;base64, ${assistant.avatar_base64}`,
      title: assistant.name,
      description: assistant.description,
      owner: 'Helsingborg',
      starters: assistant.sample_questions,
      metadata: {
        category: 'Demo',
        conversationCount: '<100',
        likes: 0
      }
    }))
  }

  const featuredExhibit =  {
    title: 'Featured Assistants',
    description: 'Our most popular AI assistants',
    cards: assistantCards.filter((card) => {
      return card.title.toLowerCase().includes('code') || card.title.toLowerCase().includes('writing')
    }),
  }

  const mathExhibit =  {
    title: 'Specialized Tools',
    description: 'Domain-specific assistants',
    cards: assistantCards.filter((card) => card.title.toLowerCase().includes('math')),
  }

  const vanillaExhibit =  {
    title: 'Vanilla Assistants',
    description: 'When you don\'t need anything extra',
    cards: assistantCards.filter((card) => card.title.toLowerCase().includes('vanilla')),
  }

  return {
    exhibits: [featuredExhibit, mathExhibit, vanillaExhibit]
  }
}
