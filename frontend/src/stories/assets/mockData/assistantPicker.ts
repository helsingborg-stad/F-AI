import type { IAssistantMenu } from '$lib/types.js'

export const mockOnlyAssistants: IAssistantMenu[] = [
  {
    menuTitle: '',
    menuItems: [
      { id: '0', name: 'Language assistant', allowSearch: false },
      { id: '1', name: 'Math assistant', allowSearch: false },
    ],
  },
]

export const mockTitleAndAssistants: IAssistantMenu[] = [
  {
    menuTitle: 'Fav',
    menuItems: [{ id: '0', name: 'Wikipedia assistant', allowSearch: false }],
  },
  {
    menuTitle: 'General',
    menuItems: [
      { id: '0', name: 'Language assistant', allowSearch: false },
      { id: '1', name: 'Math assistant', allowSearch: false },
    ],
  },
]
