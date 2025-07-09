const isBrowser = typeof window !== 'undefined'

const loadSidebarState = (): boolean => {
  if (!isBrowser) return true
  
  const saved = localStorage.getItem('showSidebar')
  if (saved !== null) {
    return saved === 'true'
  }
  
  return window.innerWidth >= 768
}

let showSidebar = $state(loadSidebarState())
let isManualOverride = $state(isBrowser && localStorage.getItem('showSidebar') !== null)

export const uiState = {
  get showSidebar() {
    return showSidebar
  },
  set showSidebar(value: boolean) {
    showSidebar = value
  },
  get isManualOverride() {
    return isManualOverride
  },
  setShowSidebarManual(value: boolean) {
    showSidebar = value
    isManualOverride = true
    if (isBrowser) {
      localStorage.setItem('showSidebar', String(value))
    }
  },
  setShowSidebarAuto(value: boolean) {
    if (!isManualOverride) {
      showSidebar = value
    }
  },
  toggleSidebar() {
    showSidebar = !showSidebar
    isManualOverride = true
    if (isBrowser) {
      localStorage.setItem('showSidebar', String(showSidebar))
    }
  },
  clearManualOverride() {
    isManualOverride = false
    if (isBrowser) {
      localStorage.removeItem('showSidebar')
      const isMobile = window.innerWidth < 768
      showSidebar = !isMobile
    }
  }
}
