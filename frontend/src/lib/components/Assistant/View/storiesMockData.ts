import type { IAssistantCard, IExhibit } from '$lib/types.ts'
import codingAssistantAvatar from '$stories/assets/avatar/coding-assistant.png'
import writingAssistantAvatar from '$stories/assets/avatar/writing-assistant.png'
import mathAssistantAvatar from '$stories/assets/avatar/math-assistant.png'

export const mockAssistantCards: IAssistantCard[] = [
  {
    id: 'mac0',
    avatar: codingAssistantAvatar,
    primaryColor: 'transparent',
    title: 'Code Assistant',
    description: 'Helps you write better code',
    owner: 'Zoo Inc',
    starters: [
      'Informera mig om vad du kan hjälpa mig med.',
      'Vad ska jag tänka på när jag besöker zoot?',
    ],
    isFavorite: false,
    metadata: {
      category: 'Zoo',
      conversationCount: '100',
      likes: '12',
    },
  },
  {
    id: 'mac1',
    avatar: writingAssistantAvatar,
    primaryColor: 'transparent',
    title: 'Writing Assistant',
    description: 'Improves your writing',
    owner: 'Zoo Inc',
    starters: [
      'Informera mig om vad du kan hjälpa mig med.',
      'Vad ska jag tänka på när jag besöker zoot?',
    ],
    isFavorite: false,
    metadata: {
      category: 'Zoo',
      conversationCount: '500+',
      likes: '32',
    },
  },
  {
    id: 'mac2',
    avatar: '',
    primaryColor: '#b18be0',
    title: 'Primary color',
    description: 'Assistant with color and no avatar',
    owner: 'Zoo Inc',
    starters: [],
    isFavorite: false,
    metadata: {
      category: 'Zoo',
      conversationCount: '500+',
      likes: '0',
    },
  },
  {
    id: 'mac3',
    avatar: '',
    primaryColor: 'transparent',
    title: 'Transparent',
    description: 'Assistant with transparent color and no avatar',
    owner: 'Zoo Inc',
    starters: [],
    isFavorite: false,
    metadata: {
      category: 'Zoo',
      conversationCount: '500+',
      likes: '0',
    },
  },
]

const mockExhibitFeatured: IExhibit = {
  title: 'Featured Assistants',
  description: 'Our most popular AI assistants',
  cards: mockAssistantCards,
}

const mockExhibitSpecialized: IExhibit = {
  title: 'Specialized Tools',
  description: 'Domain-specific assistants',
  cards: [
    {
      id: 'mes0',
      avatar: mathAssistantAvatar,
      primaryColor: 'transparent',
      title: 'Math Tutor',
      description: 'Solves complex equations',
      owner: 'Zoo Inc',
      starters: [
        'Informera mig om vad du kan hjälpa mig med.',
        'Vad ska jag tänka på när jag besöker zoot?',
      ],
      isFavorite: false,
      metadata: {
        category: 'Zoo',
        conversationCount: '1000',
        likes: '0',
      },
    },
  ],
}

export const mockExhibits: IExhibit[] = [mockExhibitFeatured, mockExhibitSpecialized]
