import type {
  IAvatarSizeConfigProvider,
  IAvatarSizeDescriptor,
} from '$lib/utils/image/contracts.js'

export class DefaultAvatarSizeConfigProvider implements IAvatarSizeConfigProvider {
  private readonly descriptors: IAvatarSizeDescriptor[] = [
    {
      name: 'avatarThumbnail',
      options: {
        width: 80,
        height: 80,
        format: 'webp',
        quality: 70,
        fit: 'cover',
      },
    },
    {
      name: 'avatarMedium',
      options: {
        width: 300,
        height: 300,
        format: 'webp',
        quality: 80,
        fit: 'inside',
      },
    },
  ]

  getAll(): IAvatarSizeDescriptor[] {
    return structuredClone(this.descriptors)
  }
}
