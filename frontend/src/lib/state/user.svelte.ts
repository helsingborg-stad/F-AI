export const userState = $state({
  authenticated: false,
  email: '',
  scopes: [] as string[],
})

export function setUser(userData: {
  authenticated: boolean
  email: string
  scopes: { scopes: string[] }
}) {
  userState.authenticated = userData.authenticated
  userState.email = userData.email
  userState.scopes = userData.scopes.scopes
}

export function clearUser() {
  userState.authenticated = false
  userState.email = ''
  userState.scopes = []
}

export function hasScope(scope: string): boolean {
  return userState.scopes.includes(scope)
}

export function hasAllScopes(requiredScopes: string[]): boolean {
  return requiredScopes.every(scope => userState.scopes.includes(scope))
}

export function hasAnyScope(possibleScopes: string[]): boolean {
  return possibleScopes.some(scope => userState.scopes.includes(scope))
}
