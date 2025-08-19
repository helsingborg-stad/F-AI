import { describe, it, expect, beforeEach } from 'vitest'
import { createAvatarProcessor } from './factory.js'
import type { IAvatarProcessor } from './contracts.js'
import type { IBackendAssistant } from '$lib/types.js'

const SAMPLE_PNG_BASE64 =
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='

describe('Avatar Processing Integration Tests', () => {
  let processor: IAvatarProcessor

  beforeEach(async () => {
    processor = await createAvatarProcessor()
  })

  it('processes a complete avatar workflow', async () => {
    const assistant: IBackendAssistant = {
      id: 'integration-test-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: SAMPLE_PNG_BASE64 },
    }

    const result1 = await processor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string,
    )

    expect(result1.avatarThumbnail).toBeTruthy()
    expect(result1.avatarMedium).toBeTruthy()
    expect(result1.avatarThumbnail).toContain('data:image/')
    expect(result1.avatarMedium).toContain('data:image/')

    const result2 = await processor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string,
    )

    expect(result2).toEqual(result1)
    expect(result2).toBe(result1)
  })

  it('handles assistant without avatar', async () => {
    const assistant: IBackendAssistant = {
      id: 'no-avatar-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: {},
    }

    const result = await processor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string | undefined,
    )

    expect(result).toEqual({
      avatarThumbnail: null,
      avatarMedium: null,
    })
  })

  it('generates properly formatted data URIs', async () => {
    const assistant: IBackendAssistant = {
      id: 'format-test-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: SAMPLE_PNG_BASE64 },
    }

    const result = await processor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string | undefined,
    )

    expect(result.avatarThumbnail).toMatch(/^data:image\/\w+;base64,/)
    expect(result.avatarMedium).toMatch(/^data:image\/\w+;base64,/)

    const thumbnailBase64 = result.avatarThumbnail!.split(',')[1]
    const mediumBase64 = result.avatarMedium!.split(',')[1]

    expect(thumbnailBase64).toBeTruthy()
    expect(mediumBase64).toBeTruthy()

    expect(() => Buffer.from(thumbnailBase64, 'base64')).not.toThrow()
    expect(() => Buffer.from(mediumBase64, 'base64')).not.toThrow()
  })

  it('handles invalid base64 input gracefully', async () => {
    const assistant: IBackendAssistant = {
      id: 'invalid-base64-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: 'invalid-base64-data' },
    }

    await expect(
      processor.process(assistant.id, assistant.meta.avatar_base64 as string),
    ).rejects.toThrow('Input buffer contains unsupported image format')
  })

  it('handles corrupted image data', async () => {
    const corruptedPngBase64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAYAAAAf'

    const assistant: IBackendAssistant = {
      id: 'corrupted-image-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: corruptedPngBase64 },
    }

    await expect(
      processor.process(assistant.id, assistant.meta.avatar_base64 as string),
    ).rejects.toThrow('Input buffer has corrupt header')
  })

  it('handles empty string differently from null/undefined', async () => {
    const assistant: IBackendAssistant = {
      id: 'empty-string-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: '' },
    }

    const result = await processor.process(
      assistant.id,
      assistant.meta.avatar_base64 as string,
    )

    expect(result).toEqual({
      avatarThumbnail: null,
      avatarMedium: null,
    })
  })

  it('handles concurrent processing of same assistant correctly', async () => {
    const assistant: IBackendAssistant = {
      id: 'concurrent-test-assistant',
      model_key: 'gpt-4',
      model: 'gpt-4',
      instructions: 'Test assistant',
      collection_id: null,
      max_collection_results: '10',
      meta: { avatar_base64: SAMPLE_PNG_BASE64 },
    }

    const promises = Array.from({ length: 3 }, () =>
      processor.process(assistant.id, assistant.meta.avatar_base64 as string)
    )

    const results = await Promise.all(promises)

    results.forEach(result => {
      expect(result.avatarThumbnail).toBeTruthy()
      expect(result.avatarMedium).toBeTruthy()
      expect(result.avatarThumbnail).toContain('data:image/')
      expect(result.avatarMedium).toContain('data:image/')
    })

    const firstResult = results[0]
    results.forEach(result => {
      expect(result).toEqual(firstResult)
    })

    const cachedResult = await processor.process(
      assistant.id, 
      assistant.meta.avatar_base64 as string
    )
    expect(cachedResult).toEqual(firstResult)
  })
})
