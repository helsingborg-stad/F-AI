import type { UserScopeType } from '$lib/types.js'
import type { RequestEvent } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export function hasScope(scope: UserScopeType, userScopes: UserScopeType[]): boolean {
  return userScopes ? userScopes.includes(scope) : false
}

export function canReadAssistants(userScopes: UserScopeType[]): boolean {
  return hasScope('assistant.read', userScopes)
}

export class UserScopeFactory {
  readonly #event: RequestEvent

  constructor(event: RequestEvent) {
    this.#event = event
  }

  async fetchScopes(): Promise<UserScopeType[]> {
    const api = new BackendApiServiceFactory().get(this.#event)
    const [error, scopes] = await api.getScopes()

    if (error) {
      console.error('Failed to fetch scopes', error)
      return []
    }

    return scopes || []
  }

  async hasScope(scopesToCheck: UserScopeType): Promise<boolean> {
    const userScopes = await this.fetchScopes()

    return userScopes.includes(scopesToCheck)
  }

  async canReadAssistants(): Promise<boolean> {
    return this.hasScope('assistant.read')
  }
}

export function createUserScopeFactory(event: RequestEvent) {
  return new UserScopeFactory(event)
}
