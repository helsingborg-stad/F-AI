import type { IAssistantCard, IExhibit } from '$lib/types.ts'
import placeholderImage from '$lib/assets/fai-avatar.png'
import codingAssistantAvatar from '$stories/assets/avatar/coding-assistant.png'
import writingAssistantAvatar from '$stories/assets/avatar/writing-assistant.png'
import mathAssistantAvatar from '$stories/assets/avatar/math-assistant.png'

export const mockAssistantCards: IAssistantCard[] = [
  {
    avatar: codingAssistantAvatar,
    title: 'Code Assistant',
    description: 'Helps you write better code',
    owner: 'Zoo Inc',
    category: 'Zoo',
    starters: [
      'Informera mig om vad du kan hjälpa mig med.',
      'Vad ska jag tänka på när jag besöker zoot?',
    ],
    conversationCount: '100'
  },
  {
    avatar: writingAssistantAvatar,
    title: 'Writing Assistant',
    description: 'Improves your writing',
    owner: 'Zoo Inc',
    category: 'Zoo',
    starters: [
      'Informera mig om vad du kan hjälpa mig med.',
      'Vad ska jag tänka på när jag besöker zoot?',
    ],
    conversationCount: '500+'
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
      avatar: mathAssistantAvatar,
      title: 'Math Tutor',
      description: 'Solves complex equations',
      owner: 'Zoo Inc',
      category: 'Zoo',
      starters: [
        'Informera mig om vad du kan hjälpa mig med.',
        'Vad ska jag tänka på när jag besöker zoot?',
      ],
      conversationCount: '1000'
    },
  ],
}

export const mockExhibits: IExhibit[] = [mockExhibitFeatured, mockExhibitSpecialized]
