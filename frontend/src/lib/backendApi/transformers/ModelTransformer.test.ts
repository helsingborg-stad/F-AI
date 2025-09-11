import { describe, it, expect } from 'vitest'
import { ModelTransformer } from './ModelTransformer.js'
import type { ModelDTO } from './ModelTransformer.js'
import type { IAssistantModel } from '$lib/types.js'

describe('ModelTransformer', () => {
  const transformer = new ModelTransformer()

  describe('toFrontend', () => {
    it('should transform snake_case fields to camelCase', () => {
      const dto: ModelDTO = {
        key: 'gpt-4',
        provider: 'OpenAI',
        display_name: 'GPT-4',
        description: 'Advanced model',
        meta: {
          primary_color: '#10A37F',
          avatar_base64: 'data:image/png;base64,abc123',
          capabilities: {
            supports_imagegen: true,
            supports_reasoning: true,
            supports_code_execution: false,
            supports_function_calling: true,
            supports_web_search: false,
            max_tokens: 128000,
          },
        },
        created_at: '2024-01-01',
        updated_at: '2024-01-02',
        status: 'active',
        visibility: 'public',
        version: 2,
      }

      const result = transformer.toFrontend(dto)

      expect(result).toEqual({
        key: 'gpt-4',
        provider: 'OpenAI',
        display_name: 'GPT-4',
        description: 'Advanced model',
        displayName: 'GPT-4',
        enhancedDescription: 'Advanced model',
        meta: {
          primaryColor: '#10A37F',
          avatar_base64: 'data:image/png;base64,abc123',
          capabilities: {
            supportsImagegen: true,
            supportsReasoning: true,
            supportsCodeExecution: false,
            supportsFunctionCalling: true,
            supportsWebSearch: false,
            maxTokens: 128000,
          },
        },
        created_at: '2024-01-01',
        updated_at: '2024-01-02',
        status: 'active',
        visibility: 'public',
        version: 2,
      })
    })

    it('should handle missing optional fields', () => {
      const dto: ModelDTO = {
        key: 'model-1',
        provider: 'Provider',
        display_name: 'Model 1',
        meta: {},
      }

      const result = transformer.toFrontend(dto)

      expect(result).toEqual({
        key: 'model-1',
        provider: 'Provider',
        display_name: 'Model 1',
        description: undefined,
        displayName: 'Model 1',
        enhancedDescription: '',
        meta: {},
      })
    })

    it('should transform nested objects in meta', () => {
      const dto: ModelDTO = {
        key: 'model-1',
        provider: 'Provider',
        display_name: 'Model 1',
        meta: {
          custom_field: 'value',
          nested_object: {
            inner_field: 'inner_value',
            deep_nested: {
              very_deep: true,
            },
          },
        },
      }

      const result = transformer.toFrontend(dto)

      expect(result.meta).toEqual({
        customField: 'value',
        nestedObject: {
          innerField: 'inner_value',
          deepNested: {
            veryDeep: true,
          },
        },
      })
    })
  })

  describe('toBackend', () => {
    it('should transform camelCase fields to snake_case', () => {
      const model: IAssistantModel = {
        key: 'claude-3',
        provider: 'Anthropic',
        display_name: 'Claude 3',
        description: 'Anthropic model',
        displayName: 'Claude 3',
        enhancedDescription: 'Anthropic model',
        meta: {
          primaryColor: '#D97757',
          avatar_base64: 'data:image/png;base64,xyz789',
          capabilities: {
            supportsImagegen: true,
            supportsReasoning: false,
            supportsCodeExecution: true,
            supportsFunctionCalling: true,
            supportsWebSearch: true,
            maxTokens: 200000,
          },
        },
        status: 'active',
        visibility: 'public',
        version: 1,
      }

      const result = transformer.toBackend(model)

      expect(result).toEqual({
        key: 'claude-3',
        provider: 'Anthropic',
        display_name: 'Claude 3',
        description: 'Anthropic model',
        meta: {
          primary_color: '#D97757',
          avatar_base64: 'data:image/png;base64,xyz789',
          capabilities: {
            supports_imagegen: true,
            supports_reasoning: false,
            supports_code_execution: true,
            supports_function_calling: true,
            supports_web_search: true,
            max_tokens: 200000,
          },
        },
        status: 'active',
        visibility: 'public',
        version: 1,
      })
    })

    it('should handle missing capabilities', () => {
      const model: IAssistantModel = {
        key: 'model-1',
        provider: 'Provider',
        display_name: 'Model 1',
        displayName: 'Model 1',
        enhancedDescription: '',
        meta: {
          primaryColor: '#000000',
        },
      }

      const result = transformer.toBackend(model)

      expect(result.meta).toEqual({
        primary_color: '#000000',
      })
    })

    it('should transform nested camelCase objects to snake_case', () => {
      const model: IAssistantModel = {
        key: 'model-1',
        provider: 'Provider',
        display_name: 'Model 1',
        displayName: 'Model 1',
        enhancedDescription: '',
        meta: {
          customField: 'value',
          nestedObject: {
            innerField: 'inner_value',
            deepNested: {
              veryDeep: false,
            },
          },
        },
      }

      const result = transformer.toBackend(model)

      expect(result.meta).toEqual({
        custom_field: 'value',
        nested_object: {
          inner_field: 'inner_value',
          deep_nested: {
            very_deep: false,
          },
        },
      })
    })
  })

  describe('bidirectional transformation', () => {
    it('should maintain data integrity through round-trip transformation', () => {
      const original: IAssistantModel = {
        key: 'test-model',
        provider: 'TestProvider',
        display_name: 'Test Model',
        description: 'A test model',
        displayName: 'Test Model',
        enhancedDescription: 'A test model',
        meta: {
          primaryColor: '#FF0000',
          avatar_base64: 'data:test',
          capabilities: {
            supportsImagegen: true,
            supportsReasoning: false,
            supportsCodeExecution: true,
            supportsFunctionCalling: false,
            supportsWebSearch: false,
            maxTokens: 8192,
          },
          customData: {
            nestedField: 'value',
            anotherNested: {
              deepField: 123,
            },
          },
        },
        status: 'deprecated',
        visibility: 'internal',
        version: 5,
      }

      const dto = transformer.toBackend(original)
      const result = transformer.toFrontend(dto)

      expect(result).toEqual(original)
    })
  })
})
