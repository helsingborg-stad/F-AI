import { redirect } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.ts'
import dayjs from 'dayjs'

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
        isIdSubmitted: true,
      }
    } else {
      return {
        email,
        isIdSubmitted: false,
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


    const cookies = response.headers.getSetCookie()
    cookies.forEach(cookie => {
      const pairs = cookie.split(';').map(v => v.split('='))
      const kvp: Record<string, string> = pairs.reduce((acc, [k, v]) => ({ ...acc, [k.trim().toLowerCase()]: v }), {})

      const cookieName = pairs[0][0]
      event.cookies.set(cookieName, kvp[cookieName], {
        path: '/',
        sameSite: 'lax',
        httpOnly: true,
        secure: true,
        expires: dayjs(kvp['expires']).toDate(),
      })
    })

    if (response.ok) {
      throw redirect(303, '/')
    } else {
      return {
        email,
        request_id: requestId,
        isIdSubmitted: true,
        error:
          'There was an error verifying your code. If the problem persists contact support for assistance.',
      }
    }
  },
}
