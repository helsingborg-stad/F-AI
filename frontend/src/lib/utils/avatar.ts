export async function getAssistantAvatar(assistantId: string, bustCache: boolean = false): Promise<string> {
  const url = new URL(`/api/assistant/${assistantId}/avatar`, window.location.origin)
  
  if (bustCache) {
    url.searchParams.set('_t', Date.now().toString())
  }
  
  const response = await fetch(url.toString())
  
  if (!response.ok) {
    throw new Error('Failed to fetch assistant avatar')
  }
  
  const data = await response.json()
  return data.avatar
}
