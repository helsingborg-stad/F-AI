import { describe, it, expect, beforeEach } from 'vitest'
import { AvatarProcessor } from './AvatarProcessor.js'
import type {
  IAvatarCache,
  IImageCompressor,
  IAvatarSizeConfigProvider,
  AvatarCacheValue,
  IAvatarSizeDescriptor,
  ImageResizeOptions,
} from '../contracts.js'

const TEST_BASE64_PNG =
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
const TEST_BASE64_CONTENT_1 = 'content1'
const TEST_BASE64_CONTENT_2 = 'content2'
const TEST_BASE64_GENERIC = 'some-base64-content'

class FakeAvatarCache implements IAvatarCache {
  private cache = new Map<string, AvatarCacheValue>()
  private getResponses = new Map<string, AvatarCacheValue | undefined>()
  private setCalls: Array<{
    assistantId: string
    hash: string
    value: AvatarCacheValue
  }> = []
  private getCalls: Array<{ assistantId: string; hash: string }> = []

  get(assistantId: string, hash: string): AvatarCacheValue | undefined {
    this.getCalls.push({ assistantId, hash })

    const key = `${assistantId}:${hash}`
    if (this.getResponses.has(key)) {
      return this.getResponses.get(key)
    }

    const wildcardKey = `${assistantId}:*`
    if (this.getResponses.has(wildcardKey)) {
      return this.getResponses.get(wildcardKey)
    }

    return this.cache.get(key)
  }

  set(assistantId: string, hash: string, value: AvatarCacheValue): void {
    this.setCalls.push({ assistantId, hash, value })
    this.cache.set(`${assistantId}:${hash}`, value)
  }

  clear(): void {
    this.cache.clear()
  }

  setCachedValue(assistantId: string, hash: string, value: AvatarCacheValue): void {
    this.cache.set(`${assistantId}:${hash}`, value)
  }

  setGetResponse(
    assistantId: string,
    hash: string,
    value: AvatarCacheValue | undefined,
  ): void {
    this.getResponses.set(`${assistantId}:${hash}`, value)
  }

  setGetResponseForAnyHash(assistantId: string, value: AvatarCacheValue): void {
    this.getResponses.set(`${assistantId}:*`, value)
  }

  getSetCalls(): Array<{ assistantId: string; hash: string; value: AvatarCacheValue }> {
    return [...this.setCalls]
  }

  getGetCalls(): Array<{ assistantId: string; hash: string }> {
    return [...this.getCalls]
  }

  resetCallTracking(): void {
    this.setCalls = []
    this.getCalls = []
    this.getResponses.clear()
  }
}

class FakeImageCompressor implements IImageCompressor {
  private responses: string[] = []
  private errors: Error[] = []
  private callIndex = 0

  async compress(base64: string, options: ImageResizeOptions): Promise<string> {
    const currentIndex = this.callIndex++

    if (this.errors[currentIndex]) {
      throw this.errors[currentIndex]
    }

    if (this.responses[currentIndex]) {
      return this.responses[currentIndex]
    }

    const format = options.format || 'jpeg'
    const size = `${options.width}x${options.height}`
    return `data:image/${format};base64,COMPRESSED_${size}_${base64.slice(0, 10)}`
  }

  setNextResponse(response: string): void {
    this.responses[this.callIndex] = response
  }

  setNextResponses(responses: string[]): void {
    responses.forEach((response, index) => {
      this.responses[this.callIndex + index] = response
    })
  }

  setNextError(error: Error): void {
    this.errors[this.callIndex] = error
  }

  reset(): void {
    this.responses = []
    this.errors = []
    this.callIndex = 0
  }
}

class FakeAvatarSizeConfigProvider implements IAvatarSizeConfigProvider {
  private sizes: IAvatarSizeDescriptor[] = []

  getAll(): IAvatarSizeDescriptor[] {
    return [...this.sizes]
  }

  setSizes(sizes: IAvatarSizeDescriptor[]): void {
    this.sizes = sizes
  }
}

describe('AvatarProcessor', () => {
  let fakeCache: FakeAvatarCache
  let fakeCompressor: FakeImageCompressor
  let fakeSizeConfig: FakeAvatarSizeConfigProvider

  let processor: AvatarProcessor

  beforeEach(() => {
    fakeCache = new FakeAvatarCache()
    fakeCompressor = new FakeImageCompressor()
    fakeSizeConfig = new FakeAvatarSizeConfigProvider()

    processor = new AvatarProcessor(fakeCache, fakeCompressor, fakeSizeConfig)
  })

  function setupStandardSizeConfig(): void {
    fakeSizeConfig.setSizes([
      {
        name: 'avatarThumbnail',
        options: { width: 80, height: 80, format: 'webp', quality: 70, fit: 'cover' },
      },
      {
        name: 'avatarMedium',
        options: { width: 300, height: 300, quality: 80, fit: 'inside' },
      },
    ])
  }

  describe('process()', () => {
    it('returns nulls when avatar is null', async () => {
      const result = await processor.process('assistant-456', null)
      expect(result).toEqual({
        avatarThumbnail: null,
        avatarMedium: null,
      })
    })

    it('returns nulls when avatar is empty string', async () => {
      const result = await processor.process('assistant-456', '')
      expect(result).toEqual({
        avatarThumbnail: null,
        avatarMedium: null,
      })
    })

    it('generates different cache keys for same assistant with different avatars', async () => {
      setupStandardSizeConfig()

      await processor.process('assistant-123', TEST_BASE64_CONTENT_1)
      await processor.process('assistant-123', TEST_BASE64_CONTENT_2)

      const getCalls = fakeCache.getGetCalls()
      expect(getCalls).toHaveLength(2)
      expect(getCalls[0].hash).not.toBe(getCalls[1].hash)
    })

    it('returns nulls when no avatar is supplied', async () => {
      const result = await processor.process('assistant-456', undefined)

      expect(result).toEqual({
        avatarThumbnail: null,
        avatarMedium: null,
      })
    })

    it('hits the cache and returns the cached value', async () => {
      const cached: AvatarCacheValue = {
        avatarThumbnail: 'data:image/webp;base64,AAA',
        avatarMedium: 'data:image/jpeg;base64,BBB',
      }

      fakeCache.setGetResponseForAnyHash('assistant-123', cached)

      const result = await processor.process('assistant-123', TEST_BASE64_PNG)

      expect(result).toBe(cached)
    })

    it('processes all sizes when cache miss', async () => {
      setupStandardSizeConfig()

      fakeCompressor.setNextResponses([
        'data:image/webp;base64,THUMB',
        'data:image/jpeg;base64,MEDIUM',
      ])

      const result = await processor.process('assistant-123', TEST_BASE64_PNG)

      expect(result).toEqual({
        avatarThumbnail: 'data:image/webp;base64,THUMB',
        avatarMedium: 'data:image/jpeg;base64,MEDIUM',
      })

      const setCalls = fakeCache.getSetCalls()
      expect(setCalls).toHaveLength(1)
      expect(setCalls[0].assistantId).toBe('assistant-123')
      expect(setCalls[0].hash).toBeDefined()
      expect(setCalls[0].value).toEqual({
        avatarThumbnail: 'data:image/webp;base64,THUMB',
        avatarMedium: 'data:image/jpeg;base64,MEDIUM',
      })
    })

    it('throws error when compression fails', async () => {
      fakeSizeConfig.setSizes([
        {
          name: 'avatarThumbnail',
          options: { width: 80, height: 80 },
        },
      ])

      const compressionError = new Error('Compression failed')
      fakeCompressor.setNextError(compressionError)

      await expect(processor.process('assistant-123', TEST_BASE64_PNG)).rejects.toThrow(
        'Compression failed',
      )
    })

    it('throws error when one compression succeeds but another fails', async () => {
      setupStandardSizeConfig()

      fakeCompressor.setNextResponse('data:image/webp;base64,THUMB')
      fakeCompressor.setNextError(new Error('Second compression failed'))

      await expect(processor.process('assistant-123', TEST_BASE64_PNG)).rejects.toThrow(
        'Second compression failed',
      )

      const setCalls = fakeCache.getSetCalls()
      expect(setCalls).toHaveLength(0)
    })

    it('generates consistent hashes for the same base64 content', async () => {
      const cached: AvatarCacheValue = {
        avatarThumbnail: 'data:image/webp;base64,AAA',
        avatarMedium: 'data:image/jpeg;base64,BBB',
      }

      fakeCache.setGetResponseForAnyHash('assistant-123', cached)

      await processor.process('assistant-123', TEST_BASE64_PNG)
      await processor.process('assistant-123', TEST_BASE64_PNG)

      const getCalls = fakeCache.getGetCalls()
      expect(getCalls).toHaveLength(2)
      expect(getCalls[0].hash).toBe(getCalls[1].hash)
    })

    it('handles empty size configuration', async () => {
      fakeSizeConfig.setSizes([])

      const result = await processor.process('assistant-123', TEST_BASE64_PNG)

      expect(result).toEqual({
        avatarThumbnail: null,
        avatarMedium: null,
      })
    })

    it('handles duplicate size descriptor names correctly', async () => {
      fakeSizeConfig.setSizes([
        {
          name: 'avatarThumbnail',
          options: { width: 80, height: 80 },
        },
        {
          name: 'avatarThumbnail',
          options: { width: 100, height: 100 },
        },
      ])

      fakeCompressor.setNextResponses([
        'data:image/webp;base64,FIRST',
        'data:image/webp;base64,SECOND',
      ])

      const result = await processor.process('assistant-123', TEST_BASE64_PNG)

      expect(result.avatarThumbnail).toBe('data:image/webp;base64,SECOND')
    })

    it('handles concurrent processing of the same avatar', async () => {
      setupStandardSizeConfig()

      const promise1 = processor.process('assistant-123', TEST_BASE64_PNG)
      const promise2 = processor.process('assistant-123', TEST_BASE64_PNG)

      const [result1, result2] = await Promise.all([promise1, promise2])

      expect(result1).toEqual(result2)
    })
  })

  describe('hash generation', () => {
    it('generates different hashes for different content', async () => {
      fakeSizeConfig.setSizes([
        {
          name: 'avatarThumbnail',
          options: { width: 80, height: 80 },
        },
      ])

      fakeCompressor.setNextResponses([
        'data:image/webp;base64,test',
        'data:image/webp;base64,test',
      ])

      await processor.process('assistant-123', TEST_BASE64_CONTENT_1)
      await processor.process('assistant-123', TEST_BASE64_CONTENT_2)

      const getCalls = fakeCache.getGetCalls()
      expect(getCalls).toHaveLength(2)
      expect(getCalls[0].hash).not.toBe(getCalls[1].hash)
    })

    it('checks cache before processing', async () => {
      setupStandardSizeConfig()

      await processor.process('assistant-123', TEST_BASE64_PNG)

      const getCalls = fakeCache.getGetCalls()
      expect(getCalls).toHaveLength(1)
      expect(getCalls[0].assistantId).toBe('assistant-123')
    })
  })
})
