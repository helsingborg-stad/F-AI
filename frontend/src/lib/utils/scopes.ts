import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.ts'
import type { UserScopeType } from '$lib/types.js'
import type { RequestEvent } from '@sveltejs/kit'

function hasScope(scope: UserScopeType, userScopes: UserScopeType[]): boolean {
  return userScopes ? userScopes.includes(scope) : false
}

async function fetchUserScopes(event: RequestEvent): Promise<UserScopeType[]> {
  console.log('fetchUserScopes called for:', event.url.pathname)

  const accessToken = event.cookies.get('access_token')
  console.log('Access token exists:', !!accessToken)

  if (!accessToken) {
    console.log('No access token, returning empty array')
    return []
  }

  console.log('Creating API instance...')
  const api = new BackendApiServiceFactory().get(event)

  console.log('Calling getScopes...')
  const [error, scopes] = await api.getScopes()
  console.log('getScopes result:', { error, scopes })

  if (error) {
    console.error('Failed to fetch scopes', error)
    return []
  }

  return scopes || []
}

export async function userCanReadAssistants(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('assistant.read', userScopes)
}

export async function userCanWriteAssistant(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('assistant.write', userScopes)
}

export async function userCanChat(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('chat', userScopes)
}

export async function userCanReadSettings(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('settings.read', userScopes)
}

export async function userCanReadCollections(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('collection.read', userScopes)
}
