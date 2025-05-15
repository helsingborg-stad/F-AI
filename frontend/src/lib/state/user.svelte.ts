import type { IUserInfo, UserScopeType } from '$lib/types.js'
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

export function hasScope(scope: UserScopeType): boolean {
  return userState.scopes ? userState.scopes.includes(scope) : false
}

export function hasAllScopes(requiredScopes: UserScopeType[]): boolean {
  return requiredScopes.every((scope) =>
    userState.scopes ? userState.scopes.includes(scope) : false,
  )
}

export function hasAnyScope(possibleScopes: UserScopeType[]): boolean {
  return possibleScopes.some((scope) =>
    userState.scopes ? userState.scopes.includes(scope) : false,
  )
}

export function canCreateAssistant(): boolean {
  return hasScope('assistant.write')
}

export function canReadAssistants(): boolean {
  return hasScope('assistant.read')
}

export function canEditAssistants(): boolean {
  return hasScope('assistant.write')
}

export function canReadApiSettings(): boolean {
  return hasScope('settings.read')
}

export function canEditApiSettings(): boolean {
  return hasScope('settings.write')
}

export function canReadCollections(): boolean {
  return hasScope('collection.read')
}

export function canEditCollections(): boolean {
  return hasScope('collection.write')
}