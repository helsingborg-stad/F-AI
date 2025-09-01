import type { PageServerLoad, Actions } from './$types.js'
import type { RequestEvent } from '@sveltejs/kit'
import {
  userCanAccessModelSettings,
  userCanReadModels,
  userCanWriteModels,
  userCanDeleteModels,
  userIsModelAdmin,
} from '$lib/utils/scopes.js'
import { redirect } from '@sveltejs/kit'
import { handleApiError } from '$lib/utils/handle-api-errors.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.ts'

export const load: PageServerLoad = async (event: RequestEvent) => {
  // Check if user has access to model settings
  if (!(await userCanAccessModelSettings(event))) {
    throw redirect(403, '/settings')
  }

  // Get model permissions
  const modelPermissions = {
    canRead: await userCanReadModels(event),
    canWrite: await userCanWriteModels(event),
    canDelete: await userCanDeleteModels(event),
    isAdmin: await userIsModelAdmin(event),
  }

  // If user can't read models, redirect
  if (!modelPermissions.canRead) {
    throw redirect(403, '/settings')
  }

  try {
    // Fetch available models using admin endpoint
    const api = new BackendApiServiceFactory().get(event)
    const [error, modelsResponse] = await api.getAllModels()

    if (error) {
      return handleApiError(error)
    }

    // Admin endpoint returns { models: IAssistantModel[] } directly
    const models = modelsResponse?.models || []

    return {
      models,
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

    const modelData = {
      key: (formData.get('key') as string) || '',
      provider: (formData.get('provider') as string) || '',
      display_name: (formData.get('display_name') as string) || '',
      description: (formData.get('description') as string) || null,
      meta: {
        description: (formData.get('meta_description') as string) || undefined,
        avatar_base64: (formData.get('avatar_base64') as string) || undefined,
      },
    }

    try {
      const api = new BackendApiServiceFactory().get(event)
      const [error] = await api.createModel(modelData)
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

    const modelData = {
      provider: (formData.get('provider') as string) || '',
      display_name: (formData.get('display_name') as string) || '',
      description: (formData.get('description') as string) || null,
      version: version,
      meta: {
        description: (formData.get('meta_description') as string) || undefined,
        avatar_base64: (formData.get('avatar_base64') as string) || undefined,
      },
    }

    try {
      const api = new BackendApiServiceFactory().get(event)
      const [error] = await api.updateModel(key, modelData)
      if (error) {
        return handleApiError(error)
      }

      return { success: true }
    } catch (error) {
      return handleApiError(error)
    }
  },

  delete: async (event) => {
    if (!(await userCanDeleteModels(event))) {
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
