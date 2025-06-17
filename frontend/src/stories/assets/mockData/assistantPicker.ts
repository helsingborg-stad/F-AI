import type { IAssistantMenu } from '$lib/types.js'

export const mockOnlyAssistants: IAssistantMenu[] = [
  {
    menuTitle: '',
    menuItems: [
      { id: '0', name: 'Language assistant' },
      { id: '1', name: 'Math assistant' },
    ],
  },
]

export const mockTitleAndAssistants: IAssistantMenu[] = [
  {
    menuTitle: 'Fav',
    menuItems: [{ id: '0', name: 'Wikipedia assistant' }],
  },
  {
    menuTitle: 'General',
    menuItems: [
      { id: '0', name: 'Language assistant' },
      { id: '1', name: 'Math assistant' },
    ],
  },
]
