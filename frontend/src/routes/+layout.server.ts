export function load({ locals }) {
  return {
    user: locals.user || { scopes: [], email: '' },
  }
}
