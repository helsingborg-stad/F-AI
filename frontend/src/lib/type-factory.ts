import type { IAssistantMenu } from '$lib/types.js'

export function createAssistantMenu(data: {
  menuTitle: string
  hidden?: boolean
  menuItems: {
    id: string
    name: string
    allowSearch?: boolean
    allowReasoning?: boolean
    hidden?: boolean
  }[]
}): IAssistantMenu {
  return {
    menuTitle: data.menuTitle,
    hidden: data.hidden ?? false,
    menuItems: data.menuItems.map((item) => ({
      ...item,
      allowSearch: item.allowSearch ?? false,
      allowReasoning: item.allowReasoning ?? false,
    })),
  }
}
