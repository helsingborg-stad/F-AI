import type { IAssistantCard, IExhibit } from '$lib/types.js'
import placeholderImage from '$lib/assets/fai-avatar.png'

export const mockAssistantCards: IAssistantCard[] = [
  {
    avatar: placeholderImage,
    title: 'Code Assistant',
    description: 'Helps you write better code',
  },
  {
    avatar: placeholderImage,
    title: 'Writing Assistant',
    description: 'Improves your writing',
  },
]

const mockExhibitFeatured: IExhibit = {
  title: 'Featured Assistants',
  description: 'Our most popular AI assistants',
  cards: mockAssistantCards,
}

const mockExhibitSpecialized = {
  title: 'Specialized Tools',
  description: 'Domain-specific assistants',
  cards: [
    {
      avatar: placeholderImage,
      title: 'Math Tutor',
      description: 'Solves complex equations',
    },
  ],
}

export const mockExhibits: IExhibit[] = [mockExhibitFeatured, mockExhibitSpecialized]
