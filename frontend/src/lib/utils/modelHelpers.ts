import type { IAssistantModel } from '$lib/types.js'
import { icons } from '$lib/components/Icon/icons.js'

export const PROVIDER_CONFIG = {
  OpenAI: {
    iconName: 'brain' as keyof typeof icons,
    primaryColor: '#10A37F',
    fallbackAvatar: generateProviderAvatar('OpenAI', '#10A37F'),
  },
  Anthropic: {
    iconName: 'brain' as keyof typeof icons,
    primaryColor: '#D97757',
    fallbackAvatar: generateProviderAvatar('Anthropic', '#D97757'),
  },
  Mistral: {
    iconName: 'brain' as keyof typeof icons,
    primaryColor: '#FF6B35',
    fallbackAvatar: generateProviderAvatar('Mistral', '#FF6B35'),
  },
  default: {
    iconName: 'circleUser' as keyof typeof icons,
    primaryColor: '#6B7280',
    fallbackAvatar: generateProviderAvatar('AI Model', '#6B7280'),
  },
} as const

const PROVIDER_DESCRIPTION_TEMPLATES = {
  OpenAI: (modelName: string) =>
    `${modelName} - Language model by OpenAI`,
  Anthropic: (modelName: string) =>
    `${modelName} - Language model by Anthropic`,
  Mistral: (modelName: string) =>
    `${modelName} - Language model by Mistral`,
  default: (modelName: string) =>
    `${modelName} - AI language model`,
} as const

function generateProviderAvatar(providerName: string, bgColor: string): string {
  const initials = providerName.substring(0, 2).toUpperCase()
  return generateTextAvatar(initials, bgColor)
}

function generateTextAvatar(text: string, bgColor: string, size: number = 64): string {
  if (typeof document === 'undefined') {
    return ''
  }

  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')!

  ctx.fillStyle = bgColor
  ctx.fillRect(0, 0, size, size)

  ctx.fillStyle = 'white'
  ctx.font = `${size * 0.4}px Arial`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(text, size / 2, size / 2)

  return canvas.toDataURL('image/png')
}

export function getModelAvatar(model: IAssistantModel): string {
  if (model.meta.avatar_base64) {
    return model.meta.avatar_base64
  }

  const providerConfig =
    PROVIDER_CONFIG[model.provider as keyof typeof PROVIDER_CONFIG] ||
    PROVIDER_CONFIG.default
  return providerConfig.fallbackAvatar
}

export function getModelIconName(model: IAssistantModel): keyof typeof icons {
  const providerConfig =
    PROVIDER_CONFIG[model.provider as keyof typeof PROVIDER_CONFIG] ||
    PROVIDER_CONFIG.default
  return providerConfig.iconName
}

export function getModelPrimaryColor(model: IAssistantModel): string {
  const providerConfig =
    PROVIDER_CONFIG[model.provider as keyof typeof PROVIDER_CONFIG] ||
    PROVIDER_CONFIG.default
  return providerConfig.primaryColor
}

export function getModelDescription(model: IAssistantModel): string {
  if (model.meta.description?.trim()) {
    return model.meta.description
  }

  if (model.description?.trim()) {
    return model.description
  }

  const template =
    PROVIDER_DESCRIPTION_TEMPLATES[
      model.provider as keyof typeof PROVIDER_DESCRIPTION_TEMPLATES
    ] || PROVIDER_DESCRIPTION_TEMPLATES.default
  return template(model.display_name || model.name || model.key)
}

export function getModelCapabilities(model: IAssistantModel) {
  if (model.meta.capabilities) {
    return model.meta.capabilities
  }

  const capabilities = {
    supportsImages: false,
    supportsReasoning: false,
    supportsCodeExecution: false,
    supportsFunctionCalling: true,
    maxTokens: 4096,
  }

  if (model.key.includes('gpt-4o')) {
    capabilities.supportsImages = true
    capabilities.supportsReasoning = true
    capabilities.maxTokens = 128000
  } else if (model.key.includes('o3')) {
    capabilities.supportsReasoning = true
    capabilities.maxTokens = 200000
  } else if (model.key.includes('gpt-3.5')) {
    capabilities.maxTokens = 16384
  }

  if (model.key.includes('claude-3')) {
    capabilities.supportsImages = true
    capabilities.maxTokens = 200000
  }

  if (model.key.includes('mistral-large')) {
    capabilities.maxTokens = 32768
  }

  return capabilities
}

export function getEnhancedModelInfo(model: IAssistantModel) {
  const description = getModelDescription(model)
  const capabilities = getModelCapabilities(model)
  const avatar = getModelAvatar(model)
  const primaryColor = getModelPrimaryColor(model)

  return {
    ...model,
    enhancedDescription: description,
    capabilities,
    avatar,
    primaryColor,
    displayName: model.display_name || model.name || model.key.split('/')[1] || model.key,
  }
}
