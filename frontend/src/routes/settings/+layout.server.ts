import { m } from '$lib/paraglide/messages.js'
import type { IMenuItem } from '$lib/types.js'
import type { RequestEvent } from '@sveltejs/kit'
import {
  userCanReadSettings,
  userCanAccessModelSettings,
  userCanReadModels,
  userCanWriteModels,
  userCanDeleteModels,
  userIsModelAdmin,
} from '$lib/utils/scopes.js'

export async function load(event: RequestEvent) {
  const sidebarMenu: IMenuItem[] = []

  // General settings - always show if user can read settings
  if (await userCanReadSettings(event)) {
    sidebarMenu.push({
      label: m.settings_general_label(),
      path: '/settings',
    })
  }

  // Model management - show if user has model settings access
  if (await userCanAccessModelSettings(event)) {
    sidebarMenu.push({
      label: m.settings_models_label(),
      path: '/settings/models',
    })
  }

  // Calculate model permissions for the pages that need them
  const modelPermissions = {
    canRead: await userCanReadModels(event),
    canWrite: await userCanWriteModels(event),
    canDelete: await userCanDeleteModels(event),
    isAdmin: await userIsModelAdmin(event),
  }

  return {
    sidebarMenu,
    modelPermissions,
  }
}
