import type { icons } from '$lib/components/Icon/icons.js'

export type JsonValue = string | number | boolean | null | JsonObject | JsonArray;
export type JsonObject = { [key: string]: JsonValue };
export type JsonArray = JsonValue[];

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
  id: string
  options: ItemOptionsType[]
  createdTimestamp: string
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
  id: string
  model_key: string
  model: string
  instructions: string
  collection_id: string | null
  meta: JsonObject
  max_collection_results: string
}

export interface IAssistant {
  id: string
  name: string
  description: string
  avatarBase64: string
  instructions: string
  model: string
  collection?: ICollection
  maxCollectionResults: string
  isPublic: boolean
  primaryColor: string
  enableSearch: boolean
}

export interface IAssistantCard {
  id: string
  avatar: string | null
  title: string
  description: string
  owner: string
  starters: string[]
  isFavorite: boolean
  primaryColor: string
  metadata: {
    category: string
    conversationCount: string
    likes: string
  }
}

export interface IAssistantMenu {
  menuTitle: string
  menuItems: {
    allowSearch: boolean
    id: string
    name: string
  }[]
}

export interface IExhibit {
  title: string
  description: string
  cards: IAssistantCard[]
}

export interface IApiSettings {
  fixedOptCode?: string
  openAiApiKey?: string
  anthropicApiKey?: string
  mistralApiKey?: string
  jwtUserSecret?: string
  jwtExpireMinutes?: string
  brevoApiUrl?: string
  brevoApiKey?: string
}

export interface IBackendApiSettings {
  settings: {
    'login.fixed_otp'?: string
    'jwt.user_secret'?: string
    'brevo.url'?: string
    'brevo.api_key'?: string
    'openai.api_key'?: string
    'anthropic.api_key'?: string
    'mistral.api_key'?: string
  }
}

export interface ICollection {
  id: string
  label: string
  embedding_model: string
  files: ICollectionFiles[]
  urls: string[]
}

export interface ICollectionFiles {
  name: string
}
