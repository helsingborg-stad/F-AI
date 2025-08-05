import { redirect } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export const actions = {
  initiateOTP: async (event) => {
    const data = await event.request.formData()
    const email = data?.get('email') || ''
    const redirectTo = data?.get('redirectTo') || '/'

    const api = new BackendApiServiceFactory().get(event)
    const [error, request_id] = await api.loginInit(email.toString())

    if (error) {
      return {
        email,
        isIdSubmitted: false,
        error: `Error: ${error}`,
        redirectTo,
      }
    }

    return {
      email,
      request_id: request_id,
      isIdSubmitted: true,
      redirectTo,
    }
  },

  confirmOTP: async (event) => {
    const data = await event.request.formData()
    const email = data?.get('email')
    const requestId = data.get('request_id') || ''
    const confirmationCode = data.get('OTPCode') || ''
    const redirectTo = data.get('redirectTo') || '/'

    const api = new BackendApiServiceFactory().get(event)
    const [error] = await api.loginConfirm(
      requestId.toString(),
      confirmationCode.toString(),
    )

    if (error) {
      return {
        email,
        request_id: requestId,
        isIdSubmitted: true,
        error:
          'There was an error verifying your code. If the problem persists contact support for assistance.',
        redirectTo,
      }
    }

    redirect(303, redirectTo.toString())
  },
}
