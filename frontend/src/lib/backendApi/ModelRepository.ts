import type { IAssistantModel, JsonObject } from '$lib/types.js'
import type { BackendApiService, ApiResult } from '$lib/backendApi/backendApi.js'
import { ModelTransformer, type ModelDTO } from './transformers/ModelTransformer.js'

export interface IModelRepository {
  getAll(): Promise<ApiResult<IAssistantModel[]>>

  getById(key: string): Promise<ApiResult<IAssistantModel>>

  create(model: IAssistantModel): Promise<ApiResult<IAssistantModel>>

  update(key: string, model: IAssistantModel): Promise<ApiResult<IAssistantModel>>

  delete(key: string): Promise<ApiResult<never>>
}

export interface CreateModelInput {
  key: string
  provider: string
  display_name: string
  description?: string | null
  meta?: JsonObject | null
  status?: 'active' | 'deprecated' | 'disabled'
  visibility?: 'public' | 'internal'
}

export interface UpdateModelInput {
  provider: string
  display_name: string
  description?: string | null
  meta?: JsonObject | null
  status?: 'active' | 'deprecated' | 'disabled'
  visibility?: 'public' | 'internal'
  version: number
}

export class ModelRepository implements IModelRepository {
  private transformer: ModelTransformer

  constructor(private api: BackendApiService) {
    this.transformer = new ModelTransformer()
  }

  async getAll(): Promise<ApiResult<IAssistantModel[]>> {
    const [error, response] = await this.api.getAllModels()

    if (error) {
      return [error, undefined] as ApiResult<IAssistantModel[]>
    }

    const transformedModels = response.models.map((model) =>
      this.transformer.toFrontend(model as unknown as ModelDTO),
    )

    return [null, transformedModels]
  }

  async getById(key: string): Promise<ApiResult<IAssistantModel>> {
    const [error, response] = await this.api.getModel(key)

    if (error) {
      return [error, undefined] as ApiResult<IAssistantModel>
    }

    const transformedModel = this.transformer.toFrontend(response as unknown as ModelDTO)
    return [null, transformedModel]
  }

  async create(model: IAssistantModel): Promise<ApiResult<IAssistantModel>> {
    const dto = this.transformer.toBackend(model)

    const createInput: CreateModelInput = {
      key: dto.key,
      provider: dto.provider,
      display_name: dto.display_name,
      description: dto.description,
      meta: dto.meta,
      status: dto.status,
      visibility: dto.visibility,
    }

    const [error, response] = await this.api.createModel(createInput)

    if (error) {
      return [error, undefined] as ApiResult<IAssistantModel>
    }

    const transformedModel = this.transformer.toFrontend(response as unknown as ModelDTO)
    return [null, transformedModel]
  }

  async update(key: string, model: IAssistantModel): Promise<ApiResult<IAssistantModel>> {
    const dto = this.transformer.toBackend(model)

    const updateInput: UpdateModelInput = {
      provider: dto.provider,
      display_name: dto.display_name,
      description: dto.description,
      meta: dto.meta,
      status: dto.status,
      visibility: dto.visibility,
      version: dto.version || 0,
    }

    const [error, response] = await this.api.updateModel(key, updateInput)

    if (error) {
      return [error, undefined] as ApiResult<IAssistantModel>
    }

    const transformedModel = this.transformer.toFrontend(response as unknown as ModelDTO)
    return [null, transformedModel]
  }

  async delete(key: string): Promise<ApiResult<never>> {
    return await this.api.deleteModel(key)
  }

  static fromApi(api: BackendApiService): ModelRepository {
    return new ModelRepository(api)
  }
}

