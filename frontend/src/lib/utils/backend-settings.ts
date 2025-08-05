import type { RequestEvent } from '@sveltejs/kit'
import type { IBackendApiSettings } from '$lib/types.js'
import { handleApiCall } from '$lib/utils/handle-api-calls.js'

export async function getSettings(event: RequestEvent): Promise<IBackendApiSettings> {
  return handleApiCall(
    event,
    (api) => api.getSettings(),
    'Failed to fetch settings',
    {
      settings: {},
    },
  )
}
