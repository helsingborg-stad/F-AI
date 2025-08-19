
export interface AvatarCacheValue {
  avatarThumbnail: string | null
  avatarMedium: string | null
}

export interface IAvatarCache {
  get(assistantId: string, avatarBase64: string): AvatarCacheValue | undefined

  set(assistantId: string, avatarBase64: string, value: AvatarCacheValue): void
}

export interface IAvatarSizeConfigProvider {
  getAll(): IAvatarSizeDescriptor[]
}

export interface IAvatarSizeDescriptor {
  name: keyof AvatarCacheValue
  options: ImageResizeOptions
}

export interface IImageCompressor {
  compress(rawBase64: string, options: ImageResizeOptions): Promise<string>
}

export interface ImageResizeOptions {
  width: number
  height: number
  format?: 'webp' | 'png' | 'jpeg' | 'avif'
  quality?: number
  fit?: 'cover' | 'inside' | 'contain'
}

export interface IAvatarProcessor {
  process(id: string, avatarBase64: string | null | undefined): Promise<AvatarCacheValue>
}
