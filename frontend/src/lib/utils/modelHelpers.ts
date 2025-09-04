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

const MODEL_DESCRIPTIONS = {
  'openai/o3-mini':
    'Latest OpenAI reasoning model optimized for complex problem-solving with enhanced speed and efficiency.',
  'openai/gpt-4o':
    'Advanced multimodal model that can process text, images, and audio with superior reasoning capabilities.',
  'openai/gpt-3.5-turbo':
    'Fast and cost-effective model ideal for most conversational AI and text generation tasks.',

  'anthropic/claude-3-7-sonnet-latest':
    "Anthropic's most capable model with excellent reasoning, coding, and analysis capabilities.",
  'anthropic/claude-3-5-sonnet-20241022':
    'High-performance model optimized for complex reasoning and creative tasks.',
  'anthropic/claude-3-5-haiku-20241022':
    'Fast, lightweight model perfect for quick responses and simple tasks.',

  'mistral/mistral-large-latest':
    "Mistral's flagship model with strong performance across diverse language tasks.",
  'mistral/mistral-medium-latest':
    'Balanced model offering good performance with efficient resource usage.',
  'mistral/mistral-small-latest':
    'Compact model ideal for basic conversational and text processing needs.',
} as const

const PROVIDER_DESCRIPTION_TEMPLATES = {
  OpenAI: (modelName: string) =>
    `OpenAI model ${modelName} - Advanced language model for conversation and text generation.`,
  Anthropic: (modelName: string) =>
    `Anthropic model ${modelName} - Constitutional AI model focused on helpful, harmless, and honest responses.`,
  Mistral: (modelName: string) =>
    `Mistral model ${modelName} - High-performance European language model for diverse AI tasks.`,
  default: (modelName: string) =>
    `AI language model ${modelName} - General-purpose conversational AI assistant.`,
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

  if (model.key in MODEL_DESCRIPTIONS) {
    return MODEL_DESCRIPTIONS[model.key as keyof typeof MODEL_DESCRIPTIONS]
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
