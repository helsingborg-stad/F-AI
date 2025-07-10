import { getContext, setContext } from 'svelte'

const SIDEBAR_CONTEXT_KEY = 'sidebar'

export interface SidebarState {
  showSidebar: boolean
  isManualOverride: boolean
  setShowSidebarManual(value: boolean): void
  setShowSidebarAuto(value: boolean): void
  toggleSidebar(): void
  clearManualOverride(): void
}

export function setSidebarContext(state: SidebarState) {
  setContext(SIDEBAR_CONTEXT_KEY, state)
}

export function getSidebarContext() {
  const context = getContext<SidebarState>(SIDEBAR_CONTEXT_KEY)
  if (!context) {
    throw new Error('Sidebar context not found. Did you forget to wrap your component in SidebarProvider?')
  }

  return context
}
