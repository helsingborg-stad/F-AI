import type { IUserInfo, UserScopeType } from '$lib/types.js'

export const userState = $state<IUserInfo>({
  email: '',
  scopes: [],
})

export function setUser(userData: IUserInfo) {
  if ('email' in userData) {
    userState.email = userData.email
  }

  if ('scopes' in userData) {
    userState.scopes = userData.scopes
  }
}

export function clearUser() {
  userState.email = ''
  userState.scopes = []
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
