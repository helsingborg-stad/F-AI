import type { IUserInfo } from '$lib/types.js'
import { browser } from '$app/environment'

// Initialize state from localStorage if available, otherwise use default
const initialState: IUserInfo = browser
  ? JSON.parse(localStorage.getItem('userState') || '{"email":"","scopes":[]}')
  : { email: '', scopes: [] }

export const userState = $state<IUserInfo>(initialState)

// Helper function to persist state to localStorage
function persistState() {
  if (browser) {
    localStorage.setItem('userState', JSON.stringify($state.snapshot(userState)))
  }
}

export function setUser(userData: IUserInfo) {
  if ('email' in userData) {
    userState.email = userData.email
  }

  if ('scopes' in userData) {
    userState.scopes = userData.scopes
  }

  persistState()
}

export function clearUser() {
  userState.email = ''
  userState.scopes = []
  persistState()
}
