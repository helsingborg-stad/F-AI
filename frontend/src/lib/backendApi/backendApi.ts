import { env } from '$env/dynamic/private'
import { type Cookies, redirect, type RequestEvent } from '@sveltejs/kit'
import dayjs from 'dayjs'
import type {
  IAssistantModels,
  IBackendApiSettings,
  IBackendAssistant,
  ICollection,
  IConversation,
  IConversations,
  IFavAssistant,
} from '$lib/types.js'

export interface CallOptions {
  body?: string | FormData
}

export type SetCookieDelegate = (
  name: string,
  value: string,
  path: string,
  sameSite: 'lax' | 'strict' | 'none',
  httpOnly: boolean,
  secure: boolean,
  expires: Date,
) => void

export type ApiResult<T> = [string, never] | [null, T]

export class BackendApiService {
  readonly #baseUrl: string
  readonly #fetchFunc: typeof fetch
  readonly #cookies: Cookies
  readonly #setCookieDelegate: SetCookieDelegate

  constructor(
    baseUrl: string,
    fetchFunc: typeof fetch,
    cookies: Cookies,
    setCookieDelegate: SetCookieDelegate,
  ) {
    this.#baseUrl = baseUrl
    this.#fetchFunc = fetchFunc
    this.#cookies = cookies
    this.#setCookieDelegate = setCookieDelegate
  }

  #setCookiesFromResponse(response: Response) {
    const cookies = response.headers.getSetCookie()
    cookies.forEach((cookie) => {
      const [cookiePair, ...attributes] = cookie.split(';')
      const [cookieName, cookieValue] = cookiePair.split('=')
      const kvp: Record<string, string> = attributes
        .map((v) => v.split('='))
        .reduce((acc, [k, v]) => ({ ...acc, [k.trim().toLowerCase()]: v }), {})

      this.#setCookieDelegate(
        cookieName,
        cookieValue,
        '/',
        'lax',
        true,
        true,
        dayjs(kvp['expires']).toDate(),
      )
    })
  }

  #makeHeaders(body?: string | FormData): HeadersInit {
    const headers = new Headers()

    if (body !== undefined && !(body instanceof FormData)) {
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

  /**
   * Executes an API call with automatic token refresh on 401 responses
   */
  async #executeWithAuth(
    method: string,
    endpoint: string,
    opt?: CallOptions,
  ): Promise<Response> {
    const url = `${this.#baseUrl}${endpoint}`
    const requestOptions = {
      method,
      headers: this.#makeHeaders(opt?.body),
      body: opt?.body instanceof FormData ? opt.body : opt?.body,
    }

    let response = await this.#fetchFunc(url, requestOptions)

    if (response.status === 401) {
      // access token could've expired, but refresh token might be valid - try refreshing
      const refreshResponse = await this.#fetchFunc(
        `${this.#baseUrl}/api/login/refresh`,
        {
          method: 'POST',
          headers: this.#makeHeaders(),
        },
      )

      if (refreshResponse.ok) {
        // this should update the access token (and refresh token)
        this.#setCookiesFromResponse(refreshResponse)

        // retry the API call again, with refreshed credentials
        response = await this.#fetchFunc(url, {
          ...requestOptions,
          headers: this.#makeHeaders(opt?.body), // remake headers with new tokens
        })
      }
    }

    if (response.status === 401) {
      // User is still logged out and unable to re-log automatically - send back to login
      redirect(303, '/login')
    }

    return response
  }

  /**
   * Call API and return raw Response object (for SSE, streaming, etc.)
   */
  async callApiRaw(
    method: string,
    endpoint: string,
    opt?: CallOptions,
  ): Promise<Response> {
    // Don't process cookies here since the response is streamed directly to the client
    return this.#executeWithAuth(method, endpoint, opt)
  }

  async callApi<TResponseData = never>(
    method: string,
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    const response = await this.#executeWithAuth(method, endpoint, opt)

    if (!response.ok) {
      try {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          const responseData = await response.json()
          return [
            responseData?.detail ?? response.statusText,
            undefined,
          ] as ApiResult<TResponseData>
        } else {
          return [response.statusText, undefined] as ApiResult<TResponseData>
        }
      } catch {
        return [response.statusText, undefined] as ApiResult<TResponseData>
      }
    }

    this.#setCookiesFromResponse(response)

    const contentType = response.headers.get('content-type')
    if (
      response.status === 204 ||
      !contentType ||
      !contentType.includes('application/json')
    ) {
      return [null, undefined as unknown as TResponseData]
    }

    try {
      const data = await response.json()
      return [null, data as TResponseData]
    } catch (error) {
      // If JSON parsing fails, return undefined as data
      console.warn('Failed to parse JSON response', error)
      return [null, undefined as unknown as TResponseData]
    }
  }

  async get<TResponseData = never>(
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('GET', endpoint, opt)
  }

  async getRaw(endpoint: string, opt?: CallOptions): Promise<Response> {
    return this.callApiRaw('GET', endpoint, opt)
  }

  async post<TResponseData = never>(
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('POST', endpoint, opt)
  }

  async put<TResponseData = never>(
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('PUT', endpoint, opt)
  }

  async patch<TResponseData = never>(
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('PATCH', endpoint, opt)
  }

  async delete<TResponseData = never>(
    endpoint: string,
    opt?: CallOptions,
  ): Promise<ApiResult<TResponseData>> {
    return this.callApi<TResponseData>('DELETE', endpoint, opt)
  }

  /***************************************************/
  /* high-level API function mappings                */
  /***************************************************/

  /** SSE Chat */

  async getChatSSE(params: {
    messageId: string
    conversationId?: string
    assistantId?: string
    features?: string
  }): Promise<Response> {
    const { messageId, conversationId, assistantId, features = '' } = params

    const url = conversationId
      ? `/api/chat/sse/${conversationId}?stored_message_id=${messageId}&features=${features}`
      : `/api/chat/sse?assistant_id=${assistantId}&stored_message_id=${messageId}&features=${features}`

    return this.getRaw(url)
  }

    async storeChatSSE(message: string): Promise<ApiResult<string>> {
    const [error, { stored_message_id }] = await this.post<{ stored_message_id: string }>(
      '/api/chat/store',
      {
        body: JSON.stringify({ message }),
      },
    )
    return [error, stored_message_id] as ApiResult<string>
  }


  /** Auth */

  async getScopes(): Promise<ApiResult<string[]>> {
    const [error, { scopes }] = await this.get<{ scopes: string[] }>('/api/auth/scopes')
    return [error, scopes] as ApiResult<string[]>
  }

  /** Login */

  async loginInit(userId: string): Promise<ApiResult<string>> {
    const [error, { request_id }] = await this.post<{ request_id: string }>(
      '/api/login/initiate',
      {
        body: JSON.stringify({ user_id: userId }),
      },
    )
    return [error, request_id] as ApiResult<string>
  }

  async loginConfirm(
    requestId: string,
    confirmationCode: string,
  ): Promise<ApiResult<never>> {
    const [error] = await this.post('/api/login/confirm', {
      body: JSON.stringify({
        request_id: requestId,
        confirmation_code: confirmationCode,
      }),
    })
    return [error, undefined] as ApiResult<never>
  }

  async logout(): Promise<ApiResult<never>> {
    const [error] = await this.post('/api/login/logout')
    return [error, undefined] as ApiResult<never>
  }

  /** Assistant */

  async getAssistants(): Promise<ApiResult<IBackendAssistant[]>> {
    const [error, { assistants }] = await this.get<{ assistants: string[] }>(
      '/api/assistant',
    )
    return [error, assistants] as ApiResult<IBackendAssistant[]>
  }

  async getMyAssistants(): Promise<ApiResult<IBackendAssistant[]>> {
    const [error, { assistants }] = await this.get<{ assistants: string[] }>(
      '/api/assistant/me',
    )
    return [error, assistants] as ApiResult<IBackendAssistant[]>
  }

  async getAssistantModels(): Promise<ApiResult<IAssistantModels[]>> {
    const [error, { models }] = await this.get<{ models: IAssistantModels[] }>(
      '/api/assistant/models',
    )
    return [error, models] as ApiResult<IAssistantModels[]>
  }

  async getAssistant(assistantId: string): Promise<ApiResult<IBackendAssistant>> {
    const [error, { assistant }] = await this.get<{ assistant: IBackendAssistant }>(
      `/api/assistant/${assistantId}`,
    )
    return [error, assistant] as ApiResult<IBackendAssistant>
  }

  async createAssistant(): Promise<ApiResult<string>> {
    const [error, { assistant_id }] = await this.post<{ assistant_id: string }>(
      '/api/assistant',
    )
    return [error, assistant_id] as ApiResult<string>
  }

  async updateAssistant(
    assistantId: string,
    updates: {
      name?: string
      description?: string
      model?: string
      instructions?: string
      model_key?: string
      collection_id?: string | null
      max_collection_results?: string
    },
  ): Promise<ApiResult<never>> {
    const [error] = await this.put(`/api/assistant/${assistantId}`, {
      body: JSON.stringify(updates),
    })
    return [error, undefined] as ApiResult<never>
  }

  async deleteAssistant(assistantId: string): Promise<ApiResult<never>> {
    const [error] = await this.delete(`/api/assistant/${assistantId}`)
    return [error, undefined] as ApiResult<never>
  }

  async updateAssistantAvatar(
    assistantId: string,
    avatar: File,
  ): Promise<ApiResult<never>> {
    const formData = new FormData()
    formData.append('file', avatar)

    const [error] = await this.put(`/api/assistant/${assistantId}/avatar`, {
      body: formData,
    })
    return [error, undefined] as ApiResult<never>
  }

  async deleteAssistantAvatar(assistantId: string): Promise<ApiResult<never>> {
    const [error] = await this.delete(`/api/assistant/${assistantId}/avatar`)
    return [error, undefined] as ApiResult<never>
  }

  async addFavoriteAssistant(assistantId: string): Promise<ApiResult<never>> {
    const [error] = await this.post(`/api/assistant/me/favorite/${assistantId}`)
    return [error, undefined] as ApiResult<never>
  }

  async deleteFavoriteAssistant(assistantId: string): Promise<ApiResult<never>> {
    const [error] = await this.delete(`/api/assistant/me/favorite/${assistantId}`)
    return [error, undefined] as ApiResult<never>
  }

  async getFavoriteAssistants(): Promise<ApiResult<IFavAssistant[]>> {
    const [error, { assistants }] = await this.get('/api/assistant/me/favorite')
    return [error, assistants] as ApiResult<IFavAssistant[]>
  }

  /** Settings */

  async getSettings(): Promise<ApiResult<IBackendApiSettings>> {
    const [error, { settings }] = await this.get<{ settings: IBackendApiSettings }>(
      '/api/settings',
    )
    return [error, { settings }] as ApiResult<IBackendApiSettings>
  }

  async updateSettings(settings: IBackendApiSettings): Promise<ApiResult<never>> {
    const [error] = await this.patch('/api/settings', {
      body: JSON.stringify(settings),
    })
    return [error, undefined] as ApiResult<never>
  }

  /** Collections */

  async createCollection(
    label: string,
    embeddingModel: string,
  ): Promise<ApiResult<string>> {
    const [error, { collection_id }] = await this.post('/api/collection', {
      body: JSON.stringify({ label, embedding_model: embeddingModel }),
    })
    return [error, collection_id] as ApiResult<string>
  }

  async getCollections(): Promise<ApiResult<ICollection[]>> {
    const [error, { collections }] = await this.get<{ collections: string[] }>(
      '/api/collection',
    )
    return [error, collections] as ApiResult<ICollection[]>
  }

  async updateCollection(collectionId: string, files: File[]): Promise<ApiResult<never>> {
    const formData = new FormData()
    files.forEach((file) => formData.append('files', file))
    formData.append('urls', '')

    const [error] = await this.put(`/api/collection/${collectionId}/content`, {
      body: formData,
    })

    return [error, undefined] as ApiResult<never>
  }

  /** Conversations */

  async getConversations(): Promise<ApiResult<IConversations>> {
    const [error, { conversations }] = await this.get<{ conversations: IConversations }>(
      '/api/conversation',
    )
    return [error, conversations] as ApiResult<IConversations>
  }

  async getConversation(conversationId: string): Promise<ApiResult<IConversation>> {
    const [error, { conversation }] = await this.get<{ conversation: IConversation }>(
      `/api/conversation/${conversationId}`,
    )
    return [error, conversation] as ApiResult<IConversation>
  }

  async deleteConversation(conversationId: string): Promise<ApiResult<never>> {
    const [error] = await this.delete(`/api/conversation/${conversationId}`)
    return [error, undefined] as ApiResult<never>
  }

  updateConversationTitle(
    conversationId: string,
    title: string,
  ): Promise<ApiResult<never>> {
    return this.patch(`/api/conversation/${conversationId}/title`, {
      body: JSON.stringify({ title }),
    })
  }
}

export class BackendApiServiceFactory {
  get(event: RequestEvent): BackendApiService {
    return new BackendApiService(
      env.SECRET_API_URL || 'http://127.0.0.1:8000/',
      event.fetch,
      event.cookies,
      (name, value, path, sameSite, httpOnly, secure, expires) => {
        event.cookies.set(name, value, {
          path,
          sameSite,
          httpOnly,
          secure,
          expires,
        })
      },
    )
  }
}
