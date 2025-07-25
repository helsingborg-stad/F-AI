import { env } from '$env/dynamic/private'
import { redirect, type RequestEvent } from '@sveltejs/kit'
import dayjs from 'dayjs'

interface ApiOptions<T = unknown> extends Omit<RequestInit, 'method' | 'body'> {
  body?: T
  withAuth?: boolean
  event: RequestEvent
}

type HttpMethod = 'GET' | 'PATCH' | 'POST' | 'PUT' | 'DELETE'

class ApiFetchFactory {
  private readonly baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async request<T>(
    method: HttpMethod,
    endpoint: string,
    options: ApiOptions<T>,
  ): Promise<Response> {
    const { body, withAuth = true, event, ...fetchOptions } = options

    const headers = new Headers(fetchOptions.headers)

    if (body instanceof FormData) {
      headers.delete('Content-Type')
    } else if (body && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json')
    }

    if (withAuth) {
      const token = event.cookies.get('access_token')
      if (token) {
        headers.set('Authorization', `Bearer ${token}`)
      }

      const refreshToken = event.cookies.get('refresh_token')
      if (refreshToken) {
        headers.append('Cookie', `refresh_token=${refreshToken};`)
      }
    }

    const url = `${this.baseUrl}${endpoint}`
    const requestOptions: RequestInit = {
      method,
      headers,
      credentials: 'include',
      ...fetchOptions,
      body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
    }

    let response = await fetch(url, requestOptions)

    if (response.status === 401) {
      const refreshResponse = await fetch(`${this.baseUrl}/api/login/refresh`,
        {
          method: 'POST',
          headers,
        })

      if (!refreshResponse.ok) {
        const redirectTo = event.url.pathname + event.url.search
        const params = new URLSearchParams({ redirectTo })
        redirect(303, `/login?${params}`)
      }

      const cookies = refreshResponse.headers.getSetCookie()
      cookies.forEach(cookie => {
        const pairs = cookie.split(';').map(v => v.split('='))
        const kvp: Record<string, string> = pairs.reduce((acc, [k, v]) => ({ ...acc, [k.trim().toLowerCase()]: v }), {})

        const cookieName = pairs[0][0]
        event.cookies.set(cookieName.toLowerCase(), kvp[cookieName.toLowerCase()], {
          path: '/',
          sameSite: 'lax',
          httpOnly: true,
          secure: true,
          expires: dayjs(kvp['expires']).toDate(),
        })
      })


      headers.set('Authorization', `Bearer ${event.cookies.get('access_token')}`)
      response = await fetch(url, requestOptions)
    }

    if (!response.ok) {
      throw response
    }

    return response
  }

  async get<T>(endpoint: string, options: ApiOptions<T>): Promise<Response> {
    return this.request<T>('GET', endpoint, options)
  }

  async patch<T>(endpoint: string, options: ApiOptions<T>): Promise<Response> {
    return this.request<T>('PATCH', endpoint, options)
  }

  async post<T>(endpoint: string, options: ApiOptions<T>): Promise<Response> {
    return this.request<T>('POST', endpoint, options)
  }

  async put<T>(endpoint: string, options: ApiOptions<T>): Promise<Response> {
    return this.request<T>('PUT', endpoint, options)
  }

  async delete<T>(endpoint: string, options: ApiOptions<T>): Promise<Response> {
    return this.request<T>('DELETE', endpoint, options)
  }
}

export const api = new ApiFetchFactory(env.SECRET_API_URL || 'http://127.0.0.1:8000/')
