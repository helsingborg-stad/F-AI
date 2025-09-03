import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.ts'
import type { UserScopeType } from '$lib/types.js'
import type { RequestEvent } from '@sveltejs/kit'

function hasScope(scope: UserScopeType, userScopes: UserScopeType[]): boolean {
  return userScopes ? userScopes.includes(scope) : false
}

async function fetchUserScopes(event: RequestEvent): Promise<UserScopeType[]> {
  const api = new BackendApiServiceFactory().get(event)

  const [error, scopes] = await api.getScopes()

  if (error) {
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

export async function userCanReadModels(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('model.read', userScopes) || hasScope('assistant.read', userScopes)
}

export async function userCanWriteModels(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('model.write', userScopes)
}

export async function userCanDeleteModels(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('model.delete', userScopes)
}

export async function userCanAccessModelSettings(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('settings.models', userScopes)
}

export async function userIsModelAdmin(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('model.admin', userScopes)
}

export async function userCanWriteCollections(event: RequestEvent): Promise<boolean> {
  const userScopes = await fetchUserScopes(event)
  return hasScope('collection.write', userScopes)
}
