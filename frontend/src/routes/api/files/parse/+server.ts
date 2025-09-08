import { json, type RequestHandler } from '@sveltejs/kit'
import { error } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export const POST: RequestHandler = async (event) => {
  const formData = await event.request.formData()
  const file = formData.get('file')

  if (!file || !(file instanceof File)) {
    error(400, 'No file provided')
  }

  const api = new BackendApiServiceFactory().get(event)
  const [apiError, apiResult] = await api.chunkFile(file)

  if (apiError) {
    error(400, apiError)
  }

  const contents = apiResult.chunks.map((c) => c.content).join('\n\n')
  return json({ contents })
}
