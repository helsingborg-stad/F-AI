import { env } from '$env/dynamic/private'
import { type Cookies, redirect, type RequestEvent } from '@sveltejs/kit'
import dayjs from 'dayjs'

export interface CallOptions {
  body?: string
}

export type SetCookieDelegate = (name: string, value: string, path: string, sameSite: 'lax' | 'strict' | 'none', httpOnly: boolean, secure: boolean, expires: Date) => void

export type ApiResult<T> = [string, never] | [null, T]

export class BackendApiService {
  readonly #baseUrl: string
  readonly #fetchFunc: typeof fetch
  readonly #cookies: Cookies
  readonly #setCookieDelegate: SetCookieDelegate

  constructor(baseUrl: string, fetchFunc: typeof fetch, cookies: Cookies, setCookieDelegate: SetCookieDelegate) {
    this.#baseUrl = baseUrl
    this.#fetchFunc = fetchFunc
    this.#cookies = cookies
    this.#setCookieDelegate = setCookieDelegate
  }

  #setCookiesFromResponse(response: Response) {
    const cookies = response.headers.getSetCookie()
    cookies.forEach(cookie => {
      // TODO: there has to be a better way to parse the cookie string
      const cookieName = cookie.split(';')[0].split('=')[0]
      const kvp: Record<string, string> = cookie
        .split(';')
        .map(v => v.split('='))
        .reduce((acc, [k, v]) => ({ ...acc, [k.trim().toLowerCase()]: v }), {})

      this.#setCookieDelegate(
        cookieName,
        kvp[cookieName],
        '/',
        'lax',
        true,
        true,
        dayjs(kvp['expires']).toDate(),
      )
    })
  }

  #makeHeaders(withContent: boolean): HeadersInit {
    const headers = new Headers()
    if (withContent) {
      headers.append('Content-Type', 'application/json')
    }

    const accessToken = this.#cookies.get('access_token')
    if (accessToken) {
      headers.append('Authorization', `Bearer ${accessToken}`)
    }

    const refreshToken = this.#cookies.get('refresh_token')
    if (refreshToken) {
      headers.append('Cookie', `refresh_token=${refreshToken};`)
    }

    return headers
  }

  async callApi<TResponseData = never>(method: string, endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    const url = `${this.#baseUrl}${endpoint}`

    let response = await this.#fetchFunc(url, {
      method,
      headers: this.#makeHeaders(opt?.body !== undefined),
      body: opt?.body,
    })

    if (response.status === 401) {
      console.log('first response is 401, refreshing token')
      // access token could've expired, but refresh token might be valid - try refreshing
      const refreshResponse = await this.#fetchFunc(`${this.#baseUrl}/api/login/refresh`, {
        method: 'POST',
        headers: this.#makeHeaders(false),
      })

      if (refreshResponse.ok) {
        // this should update the access token (and refresh token)
        this.#setCookiesFromResponse(refreshResponse)

        console.log('refreshed token, attempting request again')

        // retry the API call again, with refreshed credentials
        response = await this.#fetchFunc(url, {
          method,
          headers: this.#makeHeaders(opt?.body !== undefined),
          body: opt?.body,
        })
      }
    }

    if (!response.ok) {
      if (response.status === 401) {
        // User is still logged out and unable to re-log automatically - send back to login
        redirect(303, '/login')
      }

      try {
        const responseData = await response.json()
        console.log('response data', responseData)
        return [responseData?.detail ?? response.statusText, undefined] as ApiResult<TResponseData>
      } catch {
        // in case the response body is not legible JSON (for example 500 error)
        return [response.statusText, undefined] as ApiResult<TResponseData>
      }
    }

    this.#setCookiesFromResponse(response)

    const data = await response.json()
    return [null, data as TResponseData]
  }

  async get<TResponseData = never>(endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('GET', endpoint, opt)
  }

  async post<TResponseData = never>(endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('POST', endpoint, opt)
  }

  async put<TResponseData = never>(endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('PUT', endpoint, opt)
  }

  async patch<TResponseData = never>(endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('PATCH', endpoint, opt)
  }

  async delete<TResponseData = never>(endpoint: string, opt?: CallOptions): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('DELETE', endpoint, opt)
  }


  /***************************************************/
  /* high-level API function mappings                */

  /***************************************************/

  /** Auth */

  async getScopes(): Promise<ApiResult<string[]>> {
    const [error, { scopes }] = await this.get<{ scopes: string[] }>('/api/auth/scopes')
    return [error, scopes] as ApiResult<string[]>
  }

  /** Login */

  async loginInit(userId: string): Promise<ApiResult<string>> {
    const [error, { request_id }] = await this.post<{ request_id: string }>('/api/login/initiate', {
      body: JSON.stringify({ user_id: userId }),
    })
    return [error, request_id] as ApiResult<string>
  }

  async loginConfirm(requestId: string, confirmationCode: string): Promise<ApiResult<never>> {
    const [error] = await this.post('/api/login/confirm', {
      body: JSON.stringify({ request_id: requestId, confirmation_code: confirmationCode }),
    })
    return [error, undefined] as ApiResult<never>
  }

  async logout(): Promise<ApiResult<never>> {
    const [error] = await this.post('/api/login/logout')
    return [error, undefined] as ApiResult<never>
  }
}

export class BackendApiServiceFactory {
  get(event: RequestEvent): BackendApiService {
    return new BackendApiService(
      env.SECRET_API_URL || 'http://127.0.0.1:8000/',
      event.fetch,
      event.cookies,
      (
        name,
        value,
        path,
        sameSite,
        httpOnly,
        secure,
        expires,
      ) => {
        event.cookies.set(name, value, {
          path,
          sameSite,
          httpOnly,
          secure,
          expires,
        })
      })
  }
}
