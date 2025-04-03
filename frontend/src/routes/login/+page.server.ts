import { redirect } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'

export const actions = {
  initiateOTP: async (event) => {
    const data = await event.request.formData()
    const email = data?.get('email') || ''

    const response = await api.post('/api/login/initiate', {
      body: { user_id: email },
      withAuth: false,
      event,
    })

    if (response.ok) {
      const responseData = await response.json()

      return {
        email,
        request_id: responseData.request_id,
        isIDSubmitted: true,
      }
    } else {
      return {
        email,
        isIDSubmitted: false,
        error: `Error: ${response.status} ${response.statusText}`,
      }
    }
  },

  confirmOTP: async (event) => {
    const data = await event.request.formData()
    const email = data?.get('email')
    const requestId = data.get('request_id')
    const confirmationCode = data.get('OTPCode')

    const response = await api.post('/api/login/confirm', {
      body: { request_id: requestId, confirmation_code: confirmationCode },
      withAuth: false,
      event,
    })

    const setCookieHeader = response.headers.get('set-cookie')

    if (setCookieHeader) {
      const match = setCookieHeader.match(/access_token=([^;]+)/)
      if (match) {
        const accessToken = match[1]

        // Set the cookie in the browser
        event.cookies.set('access_token', accessToken, {
          path: '/',
          httpOnly: true,
          sameSite: 'lax',
        })
      }
    }

    if (response.ok) {
      throw redirect(303, '/')
    } else {
      return {
        email,
        request_id: requestId,
        isIDSubmitted: true,
        error: 'There was an error verifying your code. If the problem persists contact support for assistance.',
      }
    }
  },
}
