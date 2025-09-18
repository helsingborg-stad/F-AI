import type { PageServerLoad, Actions } from './$types.js'
import type { RequestEvent } from '@sveltejs/kit'
import type { JsonObject } from '$lib/types.js'
import {
  userCanReadModels,
  userCanWriteModels,
  userIsModelAdmin,
  userCanReadSettings,
} from '$lib/utils/scopes.js'
import { redirect } from '@sveltejs/kit'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.ts'

function extractCapabilities(formData: FormData) {
  return {
    supportsImagegen: formData.get('supportsImagegen') === 'true',
    supportsReasoning: formData.get('supportsReasoning') === 'true',
    supportsCodeExecution: formData.get('supportsCodeExecution') === 'true',
    supportsFunctionCalling: formData.get('supportsFunctionCalling') === 'true',
    supportsWebSearch: formData.get('supportsWebSearch') === 'true',
    maxTokens: parseInt(formData.get('maxTokens') as string) || 4096,
  }
}

function buildMetaObject(formData: FormData): JsonObject {
  const capabilities = extractCapabilities(formData)
  const meta: JsonObject = { capabilities }
  const metaDescription = formData.get('meta_description') as string
  const avatarBase64 = formData.get('avatar_base64') as string
  const primaryColor = formData.get('primaryColor') as string

  if (metaDescription) meta.description = metaDescription
  if (avatarBase64) meta.avatar_base64 = avatarBase64
  if (primaryColor) meta.primaryColor = primaryColor

  return meta
}

export const load: PageServerLoad = async (event: RequestEvent) => {
  if (!(await userCanReadSettings(event))) {
    throw redirect(403, '/settings')
  }

  const modelPermissions = {
    canRead: await userCanReadModels(event),
    canWrite: await userCanWriteModels(event),
    canDelete: await userCanWriteModels(event),
    isAdmin: await userIsModelAdmin(event),
  }

  if (!modelPermissions.canRead) {
    throw redirect(403, '/settings')
  }

  try {
    const api = new BackendApiServiceFactory().get(event)
    const [error, models] = await api.getAllModels()

    if (error) {
      return handleApiError(error)
    }

    return {
      models: models || [],
      modelPermissions,
    }
  } catch (error) {
    return handleApiError(error)
  }
}

export const actions: Actions = {
  create: async (event) => {
    if (!(await userCanWriteModels(event))) {
      throw redirect(403, '/settings')
    }

    const formData = await event.request.formData()

    const meta = buildMetaObject(formData)

    const modelData = {
      key: (formData.get('key') as string) || '',
      provider: (formData.get('provider') as string) || '',
      display_name: (formData.get('display_name') as string) || '',
      description: (formData.get('description') as string) || null,
      meta,
    }

    try {
      const api = new BackendApiServiceFactory().get(event)
      const [error] = await api.createModel({
        key: modelData.key,
        provider: modelData.provider,
        display_name: modelData.display_name,
        description: modelData.description,
        meta: modelData.meta,
        displayName: modelData.display_name || modelData.key,
        enhancedDescription: (modelData.meta?.description as string) || modelData.description || '',
      })
      if (error) {
        return handleApiError(error)
      }
      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },

  update: async (event) => {
    if (!(await userCanWriteModels(event))) {
      throw redirect(403, '/settings')
    }

    const formData = await event.request.formData()

    const key = formData.get('key') as string
    const version = parseInt(formData.get('version') as string) || 1

    const meta = buildMetaObject(formData)

    const modelData = {
      provider: (formData.get('provider') as string) || '',
      display_name: (formData.get('display_name') as string) || '',
      description: (formData.get('description') as string) || null,
      version: version,
      meta,
    }

    try {
      const api = new BackendApiServiceFactory().get(event)
      const [error] = await api.updateModel(key, {
        key: key,
        provider: modelData.provider,
        display_name: modelData.display_name,
        description: modelData.description,
        meta: modelData.meta,
        version: modelData.version,
        displayName: modelData.display_name || key,
        enhancedDescription: (modelData.meta?.description as string) || modelData.description || '',
      })
      if (error) {
        return handleApiError(error)
      }

      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },

  delete: async (event) => {
    if (!(await userCanWriteModels(event))) {
      throw redirect(403, '/settings')
    }

    const formData = await event.request.formData()
    const key = formData.get('key') as string

    try {
      const api = new BackendApiServiceFactory().get(event)
      const [error] = await api.deleteModel(key)
      if (error) {
        return handleApiError(error)
      }

      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },
}
