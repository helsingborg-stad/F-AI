import type { RequestEvent } from '@sveltejs/kit'
import { type ApiResult, BackendApiService, BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export async function handleApiCall<T>(
  event: RequestEvent,
  apiMethod: (api: BackendApiService) => Promise<ApiResult<T>>,
  errorMessage: string,
  defaultValue: T,
): Promise<T> {
  const api = new BackendApiServiceFactory().get(event)
  const [error, result] = await apiMethod(api)

  if (error) {
    console.error(errorMessage, error)
    return defaultValue
  }

  return result || defaultValue
}