import type { IImageCompressor, ImageResizeOptions } from '$lib/utils/image/contracts.js'

let sharp: typeof import('sharp') | null = null
let sharpImported = false

async function getSharp() {
  if (!sharpImported) {
    try {
      // Only import if Node.js environment and Sharp available
      if (typeof window === 'undefined' && typeof process !== 'undefined') {
        try {
          const sharpModule = await import('sharp')
          sharp = sharpModule.default || sharpModule
        } catch (importError) {
          console.error('Error importing Sharp:', importError)
          sharp = null
        }
      }
    } catch (error) {
      console.error('Error importing Sharp:', error)
      sharp = null
    }
    sharpImported = true
  }
  return sharp
}

export class SharpImageCompressor implements IImageCompressor {
  async compress(rawBase64: string, opts: ImageResizeOptions): Promise<string> {
    const sharpInstance = await getSharp()
    if (!sharpInstance) {
      throw new Error('Sharp not available.')
    }

    try {
      const input = Buffer.from(rawBase64, 'base64')

      const pipeline = sharpInstance(input)
        .resize({
          width: opts.width,
          height: opts.height,
          fit: opts.fit ?? 'inside',
          position: 'center',
        })

      switch (opts.format) {
        case 'webp':
          pipeline.webp({ quality: opts.quality ?? 80 })
          break
        case 'jpeg':
          pipeline.jpeg({ quality: opts.quality ?? 80 })
          break
        case 'png':
          pipeline.png({ quality: opts.quality ?? 80 })
          break
        case 'avif':
          pipeline.avif({ quality: opts.quality ?? 80 })
          break
        default:
          pipeline.png({ quality: opts.quality ?? 80 })
      }

      const outputBuffer = await pipeline.toBuffer()

      const format = opts.format ?? 'png'
      const mime = `image/${format}`
      const base64 = outputBuffer.toString('base64')
      return `data:${mime};base64,${base64}`
    } catch (error) {
      console.error('Error compressing image:', error)
      throw error
    }
  }
}
