import type { RequestEvent } from '@sveltejs/kit'
import type { IApiSettings, IBackendApiSettings } from '$lib/types.js'
import { api } from '$lib/api-fetch-factory.js'

export async function updateApiSettings(updates: IApiSettings, event: RequestEvent) {
  const mapApiKeys: IBackendApiSettings = {
    settings: {
      'login.fixed_otp': updates.fixedOptCode,
      'jwt.user_secret': updates.jwtUserSecret,
      'brevo.url': updates.brevoApiUrl,
      'brevo.api_key': updates.brevoApiKey,
      'openai.api_key': updates.openAiApiKey,
      'anthropic.api_key': updates.anthropicApiKey,
      'mistral.api_key': updates.mistralApiKey,
    },
  }

  const response = await api.patch('/api/settings', { event, body: mapApiKeys })

  if (!response.ok) {
    throw new Response('Failed to update settings', { status: response.status })
  }
}
