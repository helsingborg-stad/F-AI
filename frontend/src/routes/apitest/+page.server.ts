import type { PageServerLoad } from '../$types.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export const load: PageServerLoad = async (event) => {
  const api = new BackendApiServiceFactory().get(event)

  return {}
}

export const actions = {
  loginInit: async (event) => {
    console.log('loginInit')
    const api = new BackendApiServiceFactory().get(event)
    const requestId = await api.loginInit('kenth.ljung@helsingborg.se')
    return { success: true, requestId }
  },

  loginConfirm: async (event) => {
    console.log('loginConfirm')
    const data = await event.request.formData()
    const api = new BackendApiServiceFactory().get(event)
    const requestId = (data.get('requestId') ?? '') as string

    const [error] = await api.loginConfirm(requestId, '1234')

    if (error) {
      console.error('failed to get requestId', error)
      return { success: false, error }
    }

    return { success: true }
  },

  getScopes: async (event) => {
    const api = new BackendApiServiceFactory().get(event)
    const [error, scopes] = await api.getScopes()
    if (error) {
      console.error('failed to get scopes', error)
      return { success: false }
    }
    return { success: true, scopes }
  },
}
