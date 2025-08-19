import type { IAvatarProcessor } from '$lib/utils/image/contracts.js'
import { LruAvatarCache } from '$lib/utils/image/infra/LruAvatarCache.js'
import { SharpImageCompressor } from '$lib/utils/image/infra/SharpImageCompressor.js'
import { DefaultAvatarSizeConfigProvider } from '$lib/utils/image/config/DefaultAvatarSizeConfigProvider.js'
import { AvatarProcessor } from '$lib/utils/image/domain/AvatarProcessor.js'

export async function createAvatarProcessor(): Promise<IAvatarProcessor> {
  const cache = new LruAvatarCache()
  const compressor = new SharpImageCompressor()
  const sizeConfig = new DefaultAvatarSizeConfigProvider()

  return new AvatarProcessor(cache, compressor, sizeConfig)
}

let _avatarProcessor: IAvatarProcessor | null = null

export async function getAvatarProcessor(): Promise<IAvatarProcessor> {
  if (!_avatarProcessor) {
    _avatarProcessor = await createAvatarProcessor()
  }

  return _avatarProcessor
}
