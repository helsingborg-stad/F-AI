import type { UserInfo, UserScope } from '$lib/types.js'

export const userState = $state<UserInfo>({
  authenticated: false,
  email: '',
  scopes: [],
})

export function setUser(userData: UserInfo) {
  userState.authenticated = userData.authenticated
  userState.email = userData.email
  userState.scopes = userData.scopes
}

export function clearUser() {
  userState.authenticated = false
  userState.email = ''
  userState.scopes = []
}

export function hasScope(scope: UserScope): boolean {
  return userState.scopes.includes(scope)
}

export function hasAllScopes(requiredScopes: UserScope[]): boolean {
  return requiredScopes.every((scope) => userState.scopes.includes(scope))
}

export function hasAnyScope(possibleScopes: UserScope[]): boolean {
  return possibleScopes.some((scope) => userState.scopes.includes(scope))
}
