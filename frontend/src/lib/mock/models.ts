import type { IAssistantModel } from '$lib/types.js'

function enhanceModel(model: Partial<IAssistantModel>): IAssistantModel {
  return {
    ...model,
    displayName: model.display_name || model.name || model.key?.split('/')[1] || model.key || '',
    enhancedDescription: model.meta?.description?.trim() || model.description?.trim() || '',
  } as IAssistantModel
}

export const mockModels: IAssistantModel[] = [
  enhanceModel({
    key: 'openai/gpt-4o',
    provider: 'OpenAI',
    display_name: 'GPT-4o',
    name: 'GPT-4o',
    meta: {
      description:
        'Advanced multimodal model that can process text, images, and audio with superior reasoning capabilities.',
      capabilities: {
        supportsImages: true,
        supportsReasoning: true,
        supportsCodeExecution: false,
        supportsFunctionCalling: true,
        maxTokens: 128000,
      },
      primaryColor: '#10A37F',
    },
    status: 'active',
    version: 1,
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-15T10:30:00Z',
  }),
  enhanceModel({
    key: 'openai/gpt-3.5-turbo',
    provider: 'OpenAI',
    display_name: 'GPT-3.5 Turbo',
    name: 'GPT-3.5 Turbo',
    meta: {
      description:
        'Fast and cost-effective model ideal for most conversational AI and text generation tasks.',
      capabilities: {
        supportsImages: false,
        supportsReasoning: false,
        supportsCodeExecution: false,
        supportsFunctionCalling: true,
        maxTokens: 16384,
      },
    },
    status: 'active',
    version: 1,
    created_at: '2024-01-10T08:15:00Z',
    updated_at: '2024-01-10T08:15:00Z',
  }),
  enhanceModel({
    key: 'anthropic/claude-3-5-sonnet-latest',
    provider: 'Anthropic',
    display_name: 'Claude 3.5 Sonnet',
    name: 'Claude 3.5 Sonnet',
    meta: {
      description:
        "Anthropic's most capable model with excellent reasoning, coding, and analysis capabilities.",
      capabilities: {
        supportsImages: true,
        supportsReasoning: true,
        supportsCodeExecution: true,
        supportsFunctionCalling: true,
        maxTokens: 200000,
      },
      primaryColor: '#D97757',
      avatar_base64:
        'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiNGRjgwMDAiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAxOGMtNC40MSAwLTgtMy41OS04LThzMy41OS04IDgtOCA4IDMuNTkgOCA4LTMuNTkgOC04IDh6bTAtMTJjLTIuMjEgMC00IDEuNzktNCA0czEuNzkgNCA0IDQgNC0xLjc5IDQtNC0xLjc5LTQtNC00eiIvPjwvc3ZnPg==',
    },
    status: 'active',
    version: 2,
    created_at: '2024-01-20T14:45:00Z',
    updated_at: '2024-02-01T09:20:00Z',
  }),
  enhanceModel({
    key: 'mistral/mistral-large-latest',
    provider: 'Mistral',
    display_name: 'Mistral Large',
    name: 'Mistral Large',
    meta: {
      description:
        "Mistral's flagship model with strong performance across diverse language tasks.",
      capabilities: {
        supportsImages: false,
        supportsReasoning: true,
        supportsCodeExecution: false,
        supportsFunctionCalling: true,
        maxTokens: 32768,
      },
    },
    status: 'active',
    version: 1,
    created_at: '2024-01-25T11:00:00Z',
    updated_at: '2024-01-25T11:00:00Z',
  }),
  enhanceModel({
    key: 'openai/gpt-4-turbo',
    provider: 'OpenAI',
    display_name: 'GPT-4 Turbo (Deprecated)',
    name: 'GPT-4 Turbo',
    meta: {
      description: 'Previous generation GPT-4 model. Consider upgrading to GPT-4o.',
      capabilities: {
        supportsImages: true,
        supportsReasoning: true,
        supportsCodeExecution: false,
        supportsFunctionCalling: true,
        maxTokens: 128000,
      },
    },
    status: 'deprecated',
    version: 1,
    created_at: '2023-11-06T16:30:00Z',
    updated_at: '2024-01-15T10:30:00Z',
  }),
]

export const mockModelMinimal: IAssistantModel = enhanceModel({
  key: 'custom/basic-model',
  provider: 'Custom',
  display_name: 'Basic Model',
  name: 'Basic Model',
  meta: {},
})

export const mockModelWithAvatar: IAssistantModel = enhanceModel({
  key: 'anthropic/claude-3-opus',
  provider: 'Anthropic',
  display_name: 'Claude 3 Opus',
  name: 'Claude 3 Opus',
  meta: {
    description:
      "Anthropic's most powerful model for complex tasks requiring deep analysis.",
    avatar_base64:
      'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiMxMEEzN0YiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAxOGMtNC40MSAwLTgtMy41OS04LThzMy41OS04IDgtOCA4IDMuNTkgOCA4LTMuNTkgOC04IDh6bTAtMTJjLTIuMjEgMC00IDEuNzktNCA0czEuNzkgNCA0IDQgNC0xLjc5IDQtNC0xLjc5LTQtNC00eiIvPjwvc3ZnPg==',
    capabilities: {
      supportsImages: true,
      supportsReasoning: true,
      supportsCodeExecution: true,
      supportsFunctionCalling: true,
      maxTokens: 200000,
    },
  },
  status: 'active',
  version: 1,
  created_at: '2024-01-18T12:00:00Z',
  updated_at: '2024-01-18T12:00:00Z',
})

export const mockModelPermissionsFull = {
  canRead: true,
  canWrite: true,
  canDelete: true,
  isAdmin: true,
}

export const mockModelPermissionsReadOnly = {
  canRead: true,
  canWrite: false,
  canDelete: false,
  isAdmin: false,
}

export const mockModelPermissionsWrite = {
  canRead: true,
  canWrite: true,
  canDelete: false,
  isAdmin: false,
}
