import { type Actions, error, redirect } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'
import dayjs from 'dayjs'

export const actions: Actions = {
  createCollection: async (event) => {
    const api = new BackendApiServiceFactory().get(event)
    const [apiError, result] = await api.createCollection(
      `Documents ${dayjs().format('YYYY-MM-DD HH:mm')}`,
      'default',
    )

    if (apiError) {
      error(400, apiError)
    }

    redirect(303, `/document/${result}`)
  },
}
