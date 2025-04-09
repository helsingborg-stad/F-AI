export function load({ locals }) {
  return {
    user: locals.user || { authenticated: false, scopes: [], email: '' },
  }
}
