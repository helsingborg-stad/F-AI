import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ModelRepository } from './ModelRepository.js'
import type { BackendApiService, ApiResult } from '$lib/backendApi/backendApi.js'
import type { IAssistantModel } from '$lib/types.js'

describe('ModelRepository', () => {
  let mockApi: Partial<BackendApiService>
  let repository: ModelRepository

  beforeEach(() => {
    mockApi = {
      getAllModels: vi.fn(),
      getModel: vi.fn(),
      createModel: vi.fn(),
      updateModel: vi.fn(),
      deleteModel: vi.fn(),
      createModelRepository: vi.fn(),
    }
    repository = new ModelRepository(mockApi as BackendApiService)
  })

  describe('getAll', () => {
    it('should fetch and transform all models', async () => {
      const mockModels = [
        {
          key: 'model-1',
          provider: 'Provider1',
          display_name: 'Model 1',
          meta: {
            primary_color: '#FF0000',
            capabilities: {
              supports_images: true,
              max_tokens: 4096,
            },
          },
        },
        {
          key: 'model-2',
          provider: 'Provider2',
          display_name: 'Model 2',
          meta: {
            primary_color: '#00FF00',
          },
        },
      ]

      vi.mocked(mockApi.getAllModels!).mockResolvedValue([
        null,
        { models: mockModels },
      ] as ApiResult<{ models: IAssistantModel[] }>)

      const [error, result] = await repository.getAll()

      expect(error).toBeNull()
      expect(result).toHaveLength(2)
      expect(result![0].meta.primaryColor).toBe('#FF0000')
      expect(result![0].meta.capabilities?.supportsImages).toBe(true)
      expect(result![0].meta.capabilities?.maxTokens).toBe(4096)
      expect(result![1].meta.primaryColor).toBe('#00FF00')
    })

    it('should handle API errors', async () => {
      const errorMessage = 'Network error'
      vi.mocked(mockApi.getAllModels!).mockResolvedValue([
        errorMessage,
        undefined,
      ] as ApiResult<{ models: IAssistantModel[] }>)

      const [error, result] = await repository.getAll()

      expect(error).toBe(errorMessage)
      expect(result).toBeUndefined()
    })
  })

  describe('getById', () => {
    it('should fetch and transform a single model', async () => {
      const mockModel = {
        key: 'gpt-4',
        provider: 'OpenAI',
        display_name: 'GPT-4',
        meta: {
          primary_color: '#10A37F',
          capabilities: {
            supports_images: true,
            supports_reasoning: true,
            max_tokens: 128000,
          },
        },
      }

      vi.mocked(mockApi.getModel!).mockResolvedValue([
        null,
        mockModel,
      ] as ApiResult<IAssistantModel>)

      const [error, result] = await repository.getById('gpt-4')

      expect(error).toBeNull()
      expect(result).toBeDefined()
      expect(result!.key).toBe('gpt-4')
      expect(result!.meta.primaryColor).toBe('#10A37F')
      expect(result!.meta.capabilities?.supportsImages).toBe(true)
      expect(result!.meta.capabilities?.supportsReasoning).toBe(true)
      expect(result!.meta.capabilities?.maxTokens).toBe(128000)
    })
  })

  describe('create', () => {
    it('should transform model to backend format and create', async () => {
      const inputModel: IAssistantModel = {
        key: 'new-model',
        provider: 'NewProvider',
        display_name: 'New Model',
        description: 'A new model',
        meta: {
          primaryColor: '#0000FF',
          capabilities: {
            supportsImages: false,
            maxTokens: 8192,
          },
        },
      }

      const createdModel = {
        ...inputModel,
        meta: {
          primary_color: '#0000FF',
          capabilities: {
            supports_images: false,
            max_tokens: 8192,
          },
        },
        created_at: '2024-01-01',
      }

      vi.mocked(mockApi.createModel!).mockResolvedValue([
        null,
        createdModel,
      ] as ApiResult<IAssistantModel>)

      const [error, result] = await repository.create(inputModel)

      expect(error).toBeNull()
      expect(result).toBeDefined()
      expect(result!.key).toBe('new-model')
      expect(result!.meta.primaryColor).toBe('#0000FF')
      expect(vi.mocked(mockApi.createModel!)).toHaveBeenCalledWith({
        key: 'new-model',
        provider: 'NewProvider',
        display_name: 'New Model',
        description: 'A new model',
        meta: {
          primary_color: '#0000FF',
          capabilities: {
            supports_images: false,
            max_tokens: 8192,
          },
        },
        status: undefined,
        visibility: undefined,
      })
    })
  })

  describe('update', () => {
    it('should transform model to backend format and update', async () => {
      const inputModel: IAssistantModel = {
        key: 'existing-model',
        provider: 'Provider',
        display_name: 'Updated Model',
        description: 'Updated description',
        meta: {
          primaryColor: '#FFFF00',
          capabilities: {
            supportsImages: true,
            supportsReasoning: true,
            maxTokens: 16384,
          },
        },
        version: 3,
      }

      const updatedModel = {
        ...inputModel,
        meta: {
          primary_color: '#FFFF00',
          capabilities: {
            supports_images: true,
            supports_reasoning: true,
            max_tokens: 16384,
          },
        },
        updated_at: '2024-01-02',
      }

      vi.mocked(mockApi.updateModel!).mockResolvedValue([
        null,
        updatedModel,
      ] as ApiResult<IAssistantModel>)

      const [error, result] = await repository.update('existing-model', inputModel)

      expect(error).toBeNull()
      expect(result).toBeDefined()
      expect(result!.meta.primaryColor).toBe('#FFFF00')
      expect(vi.mocked(mockApi.updateModel!)).toHaveBeenCalledWith('existing-model', {
        provider: 'Provider',
        display_name: 'Updated Model',
        description: 'Updated description',
        meta: {
          primary_color: '#FFFF00',
          capabilities: {
            supports_images: true,
            supports_reasoning: true,
            max_tokens: 16384,
          },
        },
        status: undefined,
        visibility: undefined,
        version: 3,
      })
    })
  })

  describe('delete', () => {
    it('should delete a model by key', async () => {
      vi.mocked(mockApi.deleteModel!).mockResolvedValue([
        null,
        undefined,
      ] as ApiResult<never>)

      const [error] = await repository.delete('model-to-delete')

      expect(error).toBeNull()
      expect(vi.mocked(mockApi.deleteModel!)).toHaveBeenCalledWith('model-to-delete')
    })

    it('should handle delete errors', async () => {
      const errorMessage = 'Model not found'
      vi.mocked(mockApi.deleteModel!).mockResolvedValue([
        errorMessage,
        undefined,
      ] as ApiResult<never>)

      const [error] = await repository.delete('non-existent')

      expect(error).toBe(errorMessage)
    })
  })

  describe('fromApi', () => {
    it('should create a repository instance from API service', () => {
      const repo = ModelRepository.fromApi(mockApi as BackendApiService)
      expect(repo).toBeInstanceOf(ModelRepository)
    })
  })
})