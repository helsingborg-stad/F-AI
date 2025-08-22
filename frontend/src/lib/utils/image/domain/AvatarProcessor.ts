import type {
  AvatarCacheValue,
  IAvatarCache,
  IAvatarProcessor,
  IAvatarSizeConfigProvider,
  IImageCompressor,
} from '$lib/utils/image/contracts.js'
export class AvatarProcessor implements IAvatarProcessor {
  constructor(
    private readonly _cache: IAvatarCache,
    private readonly _compressor: IImageCompressor,
    private readonly _sizeConfig: IAvatarSizeConfigProvider,
  ) {
  }

  async process(id: string, avatarBase64: string | null | undefined): Promise<AvatarCacheValue> {
    if (!avatarBase64) {
      console.log('No avatar supplied, return nulls for id', id)
      return {
        avatarThumbnail: null,
        avatarMedium: null,
      }
    }

    const cachedAvatar = this._cache.get(id, avatarBase64)
    if (cachedAvatar) {
      return cachedAvatar
    }

    const sizeDescriptors = this._sizeConfig.getAll()

    try {
      const promises = sizeDescriptors.map(async (descriptor) => {
        const dataUri = await this._compressor.compress(avatarBase64, descriptor.options)
        return [descriptor.name, dataUri] as const
      })

      const entries = await Promise.all(promises)

      const result = entries.reduce<AvatarCacheValue>((acc, [key, uri]) => {
        acc[key as keyof AvatarCacheValue] = uri
        return acc
      }, { avatarThumbnail: null, avatarMedium: null })

      this._cache.set(id, avatarBase64, result)

      return result
    } catch (error) {
      console.error('Error processing avatar:', error)
      throw error
    }
  }
}
