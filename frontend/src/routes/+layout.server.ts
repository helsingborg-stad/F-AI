export function load({ locals }) {
  return {
    user: locals.user || { scopes: [], email: '' },
    avatarMenu: [{title: 'Logout', action: '/logout' }]
  }
}
