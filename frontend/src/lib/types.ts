import type { icons } from '$lib/components/Icon/icons.js'

export interface IMenuItem {
  label: string
  path: string
}

export type ItemOptionsType = {
  iconName: keyof typeof icons
  title: string
  onClick: () => void
}

export type HistoryItemType = {
  title: string
  itemOptions: ItemOptionsType[]
  created: Date
}

export type UserScopeType =
  | 'collection.read'
  | 'collection.write'
  | 'settings.read'
  | 'document.chunk'
  | 'settings.write'
  | 'group.write'
  | 'apiKey.write'
  | 'apiKey.read'
  | 'group.read'
  | 'test'
  | 'llm.run'
  | string // Allow for future scopes

export interface IUserInfo {
  email?: string
  scopes?: UserScopeType[]
}

export interface IScopesResponse {
  scopes: UserScopeType[]
}

export interface IAssistantModel {
  key: string
  provider: string
  name: string
}

export interface IAssistantModels {
  models: IAssistantModel[]
}

export interface IBackendAssistant {
  model_key: string
  name: string
  description: string
  instructions: string
  model: string
  is_public: boolean
}

export interface IAssistant {
  id: string
  name: string
  description: string
  instructions: string
  model: string
  collection_id: string
}

export interface IAssistants {
  assistants: IAssistant[]
}

export interface IApiSettings {
  fixedOptCode: string
  openAiApiKey: string
  jwtUserSecret: string
  jwtExpireMinutes: string
  brevoApiUrl: string
  brevoApiKey: string
}
