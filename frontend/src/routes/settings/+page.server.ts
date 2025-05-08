import type { PageServerLoad } from './$types.js'
import { getSettings } from '$lib/utils/backend-settings.js'
import type { RequestEvent } from '@sveltejs/kit'

export const load: PageServerLoad = async (event: RequestEvent) => {
  try {
    const settingsData = await getSettings(event)
    const apiSettings = {
      fixedPin: settingsData.settings['login.fixed_otp'] || '',
      openAiApiKey: settingsData.settings['openai.apikey'] || '',
      jwtUserSecret: settingsData.settings['jwt.user_secret'] || null,
      jwtExpireMinutes: settingsData.settings['jwt.expire_minutes'] || null,
      brevoApiUrl: settingsData.settings['brevo.url'] || '',
      brevoApiKey: settingsData.settings['brevo.apikey'] || '',
    }

    return { settings: apiSettings }
  } catch (error) {
    console.log('Could not fetch settings: ', error)
  }
}
