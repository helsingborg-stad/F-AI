import type { PageServerLoad } from './$types.js'
import { getSettings } from '$lib/utils/backend-settings.js'
import type { RequestEvent } from '@sveltejs/kit'
import type { IApiSettings } from '$lib/types.js'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import { updateApiSettings } from '$lib/utils/api-settings.js'
import { userCanReadSettings } from '$lib/utils/scopes.js'

export const load: PageServerLoad = async (event: RequestEvent) => {
  const canReadSettings = await userCanReadSettings(event)

  if (!canReadSettings) {
    const error = new Error('You do not have permission to view settings')
    return handleApiError(error)
  }

  try {
    const settingsData = await getSettings(event)

    const apiSettings: IApiSettings = {
      fixedOptCode: settingsData.settings['login.fixed_otp'] || '',
      openAiApiKey: settingsData.settings['openai.api_key'] || '',
      anthropicApiKey: settingsData.settings['anthropic.api_key'] || '',
      mistralApiKey: settingsData.settings['mistral.api_key'] || '',
      jwtUserSecret: settingsData.settings['jwt.user_secret'] || '',
      jwtExpireMinutes: settingsData.settings['jwt.expire_minutes'] || '',
      brevoApiUrl: settingsData.settings['brevo.url'] || '',
      brevoApiKey: settingsData.settings['brevo.api_key'] || '',
    }

    return { settings: apiSettings }
  } catch (error) {
    return handleApiError(error)
  }
}

export const actions = {
  update: async (event) => {
    const formData = await event.request.formData()

    const apiSettings: IApiSettings = {
      fixedOptCode: (formData.get('fixedOptCode') as string) || '',
      openAiApiKey: (formData.get('openAiApiKey') as string) || '',
      anthropicApiKey: (formData.get('anthropicApiKey') as string) || '',
      mistralApiKey: (formData.get('mistralApiKey') as string) || '',
      jwtUserSecret: (formData.get('jwtUserSecret') as string) || '',
      jwtExpireMinutes: (formData.get('jwtExpireMinutes') as string) || '',
      brevoApiUrl: (formData.get('brevoApiUrl') as string) || '',
      brevoApiKey: (formData.get('brevoApiKey') as string) || '',
    }

    try {
      await updateApiSettings(apiSettings, event)
    } catch (error) {
      return handleApiError(error)
    }
  },
}
