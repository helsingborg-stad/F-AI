import type { IAssistantMenu } from '$lib/types.js'
import { createAssistantMenu } from '$lib/type-factory.js'

const assistantMenuWithoutTitle = createAssistantMenu({
  menuTitle: '',
  menuItems: [
    { id: '0', name: 'Language assistant' },
    { id: '1', name: 'Math assistant' },
  ],
})

const favAssistants = createAssistantMenu({
  menuTitle: 'Fav',
  menuItems: [{ id: '0', name: 'Wikipedia assistant' }],
})

const generalAssistants = createAssistantMenu({
  menuTitle: 'General',
  menuItems: [
    { id: '0', name: 'Language assistant' },
    { id: '1', name: 'Math assistant' },
  ],
})

const hiddenAssistants = createAssistantMenu({
  menuTitle: 'Hidden',
  hidden: true,
  menuItems: [{ id: '0', name: 'Language assistant' }],
})

export const mockOnlyAssistants: IAssistantMenu[] = [assistantMenuWithoutTitle]
export const mockTitleAndAssistants: IAssistantMenu[] = [favAssistants, generalAssistants]
export const mockWithHiddenAssistants: IAssistantMenu[] = [
  favAssistants,
  hiddenAssistants,
]
