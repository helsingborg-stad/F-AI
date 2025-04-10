import { redirect, type RequestEvent } from '@sveltejs/kit'

export async function handleAccess(
  event: RequestEvent<Partial<Record<string, string>>, string | null>,
) {
  const path = event.url.pathname
  const publicPaths = ['/login']

  const isPublicPath = publicPaths.some((publicPath) => publicPath === path)
  const accessToken = event.cookies.get('access_token')

  if (!isPublicPath && !accessToken) {
    return redirect(303, '/login')
  }

  return event
}
