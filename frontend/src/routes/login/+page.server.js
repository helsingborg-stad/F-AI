import { SECRET_API_URL } from '$env/static/private'
import { redirect } from '@sveltejs/kit'

export const actions = {
  initiateOTP: async ({ request }) => {
    const data = await request.formData()

    const response = await fetch(`${SECRET_API_URL}/api/login/initiate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: data.get('email') }),
    })

    const responseData = await response.json()

    return {
      email: data.get('email'),
      request_id: responseData.request_id,
      isIDSubmitted: true,
    }
  },

  confirmOTP: async ({ request, cookies }) => {
    const data = await request.formData()

    const response = await fetch(`${SECRET_API_URL}/api/login/confirm`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        request_id: data.get('request_id'),
        confirmation_code: data.get('OTPCode'),
      }),
    })

    const setCookieHeader = response.headers.get('set-cookie')

    if (setCookieHeader) {
      const match = setCookieHeader.match(/access_token=([^;]+)/);
      if (match) {
        const accessToken = match[1]

        // Set the cookie in the browser
        cookies.set('access_token', accessToken, {
          path: '/',
          httpOnly: true,
          sameSite: 'lax'
        })
      }
    }

    if (response.ok) {
      throw redirect(303, '/')
    }
  },
}
