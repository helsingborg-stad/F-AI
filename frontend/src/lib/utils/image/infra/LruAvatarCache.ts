import { LRUCache } from 'lru-cache'
import type { AvatarCacheValue, IAvatarCache } from '$lib/utils/image/contracts.js'
import { createHash } from 'crypto'

export class LruAvatarCache implements IAvatarCache {
  private cache: LRUCache<string, AvatarCacheValue>

  constructor() {
    this.cache = new LRUCache<string, AvatarCacheValue>({
      max: Number(5_000),
      ttl: Number(60 * 60 * 1000), // 1h
    })
  }

  private makeKey(assistantId: string, avatarBase64: string): string {
    const hash = createHash('sha1').update(avatarBase64).digest('hex')
    return `assistant:${assistantId}:avatar:${hash}`
  }

  get(assistantId: string, avatarBase64: string): AvatarCacheValue | undefined {
    const key = this.makeKey(assistantId, avatarBase64)
    return this.cache.get(key)
  }

  set(assistantId: string, avatarBase64: string, value: AvatarCacheValue): void {
    const key = this.makeKey(assistantId, avatarBase64)
    this.cache.set(key, value)
  }
}
