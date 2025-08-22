import { json, type RequestHandler } from '@sveltejs/kit'
import { userCanReadAssistants } from '$lib/utils/scopes.js'
import { fetchAssistantById } from '$lib/utils/assistant.js'
import { getAvatarProcessor } from '$lib/utils/image/factory.js'

export const GET: RequestHandler = async (event) => {
  const canRead = await userCanReadAssistants(event)
  if (!canRead) {
    return json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { id } = event.params

  try {
    const assistant = await fetchAssistantById(event, id as string)

    if (!assistant) {
      return json({ error: 'Assistant not found' }, { status: 404 })
    }

    const avatarProcessor = await getAvatarProcessor()
    const processedAvatar = await avatarProcessor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string | undefined,
    )

    return json({
      avatar: processedAvatar.avatarMedium,
    })
  } catch (error) {
    console.error('Error fetching avatar:', error)
    return json({ error: 'Failed to fetch avatar' }, { status: 500 })
  }
}
