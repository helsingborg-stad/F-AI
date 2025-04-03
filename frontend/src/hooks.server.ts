import { type Handle, redirect } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
  const path = event.url.pathname
  const publicPaths = ['/login']

  const isPublicPath = publicPaths.some((publicPath) => publicPath === path)

  if (!isPublicPath && !event.cookies.get('access_token')) {
    return redirect(303, '/login')
  }

  const response = await resolve(event)

  if (response.status === 401) {
    return redirect(303, '/login')
  }

  return response
}
