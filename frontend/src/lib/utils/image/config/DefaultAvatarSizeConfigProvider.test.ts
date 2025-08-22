import { describe, it, expect, beforeEach } from 'vitest'
import { DefaultAvatarSizeConfigProvider } from '$lib/utils/image/config/DefaultAvatarSizeConfigProvider.js'

describe('DefaultAvatarSizeConfigProvider', () => {
  let provider: DefaultAvatarSizeConfigProvider

  beforeEach(() => {
    provider = new DefaultAvatarSizeConfigProvider()
  })

  describe('getAll()', () => {
    it('returns all configured avatar size descriptors', () => {
      const descriptors = provider.getAll()

      expect(descriptors).toHaveLength(2)

      const thumbnail = descriptors.find((d) => d.name === 'avatarThumbnail')
      expect(thumbnail).toBeDefined()
      expect(thumbnail?.options).toEqual({
        width: 80,
        height: 80,
        format: 'webp',
        quality: 70,
        fit: 'cover',
      })

      const medium = descriptors.find((d) => d.name === 'avatarMedium')
      expect(medium).toBeDefined()
      expect(medium?.options).toEqual({
        width: 300,
        height: 300,
        format: 'webp',
        quality: 80,
        fit: 'inside',
      })
    })

    it('returns a new array each time to prevent external mutation', () => {
      const first = provider.getAll()
      const second = provider.getAll()

      expect(first).toEqual(second)
      expect(first).not.toBe(second)

      first.push({
        name: 'avatarMedium',
        options: { width: 999, height: 999 },
      })

      expect(provider.getAll()).toHaveLength(2)
      expect(second).toHaveLength(2)
    })

    it('thumbnail has smaller dimensions than medium', () => {
      const descriptors = provider.getAll()
      const thumbnail = descriptors.find((d) => d.name === 'avatarThumbnail')
      const medium = descriptors.find((d) => d.name === 'avatarMedium')

      expect(thumbnail?.options.width).toBeLessThan(medium?.options.width || 0)
      expect(thumbnail?.options.height).toBeLessThan(medium?.options.height || 0)
    })

    it('returns descriptors with unique names', () => {
      const descriptors = provider.getAll()
      const names = descriptors.map(d => d.name)
      const uniqueNames = new Set(names)

      expect(uniqueNames.size).toBe(names.length)
    })

    it('descriptor objects are deeply immutable', () => {
      const first = provider.getAll()
      const second = provider.getAll()

      first[0].options.width = 999

      const third = provider.getAll()
      expect(third[0].options.width).toBe(80)
      expect(second[0].options.width).toBe(80)
    })

    it('all descriptors have required properties', () => {
      const descriptors = provider.getAll()

      descriptors.forEach((descriptor) => {
        expect(descriptor).toHaveProperty('name')
        expect(descriptor).toHaveProperty('options')
        expect(descriptor.options).toHaveProperty('width')
        expect(descriptor.options).toHaveProperty('height')
      })
    })
  })
})
