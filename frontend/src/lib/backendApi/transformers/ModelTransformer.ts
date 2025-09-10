import type { IAssistantModel, JsonObject, JsonValue } from '$lib/types.js'

export interface ModelDTO {
  key: string
  provider: string
  display_name: string
  description?: string | null
  meta: JsonObject
  created_at?: string
  updated_at?: string
  status?: 'active' | 'deprecated' | 'disabled'
  visibility?: 'public' | 'internal'
  version?: number
  name?: string
}

export interface ModelCapabilitiesDTO {
  supports_images?: boolean
  supports_reasoning?: boolean
  supports_code_execution?: boolean
  supports_function_calling?: boolean
  max_tokens?: number
}

export interface ModelCapabilities {
  supportsImages?: boolean
  supportsReasoning?: boolean
  supportsCodeExecution?: boolean
  supportsFunctionCalling?: boolean
  maxTokens?: number
}

export class ModelTransformer {
  toFrontend(dto: ModelDTO): IAssistantModel {
    const transformedMeta = this.transformMetaToFrontend(dto.meta || {})
    
    const model: IAssistantModel = {
      key: dto.key,
      provider: dto.provider,
      display_name: dto.display_name,
      description: dto.description,
      meta: transformedMeta,
      displayName: dto.display_name || dto.name || dto.key.split('/')[1] || dto.key,
      enhancedDescription: (transformedMeta.description as string)?.trim() || dto.description?.trim() || '',
    }

    if (dto.created_at) model.created_at = dto.created_at
    if (dto.updated_at) model.updated_at = dto.updated_at
    if (dto.status) model.status = dto.status
    if (dto.visibility) model.visibility = dto.visibility
    if (dto.version !== undefined) model.version = dto.version
    if (dto.name) model.name = dto.name

    return model
  }

  toBackend(model: IAssistantModel): ModelDTO {
    const dto: ModelDTO = {
      key: model.key,
      provider: model.provider,
      display_name: model.display_name,
      description: model.description,
      meta: this.transformMetaToBackend(model.meta || {}),
    }

    if (model.created_at) dto.created_at = model.created_at
    if (model.updated_at) dto.updated_at = model.updated_at
    if (model.status) dto.status = model.status
    if (model.visibility) dto.visibility = model.visibility
    if (model.version !== undefined) dto.version = model.version
    if (model.name) dto.name = model.name

    return dto
  }

  private transformMetaToFrontend(meta: JsonObject): Record<string, JsonValue | undefined> {
    const transformed: Record<string, JsonValue | undefined> = {}
    
    for (const [key, value] of Object.entries(meta)) {
      if (key === 'primary_color') {
        transformed.primaryColor = value
      } else if (key === 'avatar_base64') {
        transformed.avatar_base64 = value
      } else if (key === 'capabilities' && value && typeof value === 'object') {
        transformed.capabilities = this.transformCapabilitiesToFrontend(value as ModelCapabilitiesDTO) as JsonValue
      } else {
        const camelKey = this.snakeToCamel(key)
        transformed[camelKey] = this.transformValue(value, 'toFrontend')
      }
    }

    return transformed as JsonObject
  }

  private transformMetaToBackend(meta: Record<string, JsonValue | undefined>): JsonObject {
    const transformed: JsonObject = {}
    
    for (const [key, value] of Object.entries(meta)) {
      if (value === undefined) continue
      
      if (key === 'primaryColor') {
        transformed.primary_color = value
      } else if (key === 'avatar_base64') {
        transformed.avatar_base64 = value
      } else if (key === 'capabilities' && value && typeof value === 'object') {
        transformed.capabilities = this.transformCapabilitiesToBackend(value as ModelCapabilities) as JsonValue
      } else {
        const snakeKey = this.camelToSnake(key)
        transformed[snakeKey] = this.transformValue(value, 'toBackend')
      }
    }

    return transformed as JsonObject
  }

  private transformCapabilitiesToFrontend(dto: ModelCapabilitiesDTO): ModelCapabilities {
    return {
      supportsImages: dto.supports_images,
      supportsReasoning: dto.supports_reasoning,
      supportsCodeExecution: dto.supports_code_execution,
      supportsFunctionCalling: dto.supports_function_calling,
      maxTokens: dto.max_tokens,
    }
  }

  private transformCapabilitiesToBackend(capabilities: ModelCapabilities): ModelCapabilitiesDTO {
    return {
      supports_images: capabilities.supportsImages,
      supports_reasoning: capabilities.supportsReasoning,
      supports_code_execution: capabilities.supportsCodeExecution,
      supports_function_calling: capabilities.supportsFunctionCalling,
      max_tokens: capabilities.maxTokens,
    }
  }

  private transformValue(value: JsonValue, direction: 'toFrontend' | 'toBackend'): JsonValue {
    if (value === null || value === undefined) {
      return value
    }

    if (Array.isArray(value)) {
      return value.map(item => this.transformValue(item, direction))
    }

    if (typeof value === 'object') {
      const transformed: JsonObject = {}
      for (const [k, v] of Object.entries(value as JsonObject)) {
        const transformedKey = direction === 'toFrontend' 
          ? this.snakeToCamel(k) 
          : this.camelToSnake(k)
        transformed[transformedKey] = this.transformValue(v, direction)
      }
      return transformed as JsonObject
    }

    return value
  }

  private snakeToCamel(str: string): string {
    return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
  }

  private camelToSnake(str: string): string {
    return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`).replace(/^_/, '')
  }
}
