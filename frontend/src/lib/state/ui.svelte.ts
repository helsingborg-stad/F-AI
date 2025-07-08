let showSidebar = $state(true)

export const uiState = {
  get showSidebar() {
    return showSidebar
  },
  set showSidebar(value: boolean) {
    showSidebar = value
  },
  toggleSidebar() {
    showSidebar = !showSidebar
  }
}
