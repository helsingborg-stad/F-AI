import type { IUserInfo, UserScopeType } from '$lib/types.js'

export const userState = $state<IUserInfo>({
  authenticated: false,
  email: '',
  scopes: [],
})

export function setUser(userData: IUserInfo) {
  userState.authenticated = userData.authenticated
  userState.email = userData.email
  userState.scopes = userData.scopes
}

export function clearUser() {
  userState.authenticated = false
  userState.email = ''
  userState.scopes = []
}

export function hasScope(scope: UserScopeType): boolean {
  return userState.scopes.includes(scope)
}

export function hasAllScopes(requiredScopes: UserScopeType[]): boolean {
  return requiredScopes.every((scope) => userState.scopes.includes(scope))
}

export function hasAnyScope(possibleScopes: UserScopeType[]): boolean {
  return possibleScopes.some((scope) => userState.scopes.includes(scope))
}
