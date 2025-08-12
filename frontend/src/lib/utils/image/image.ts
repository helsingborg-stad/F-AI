/* -----------------------------------------------------------------------
 *  image‑utils.ts
 * ---------------------------------------------------------------------*/

import sharp, { type Sharp } from 'sharp'
// import LRU from 'lru-cache'; // npm i lru-cache
import { LRUCache} from 'lru-cache'
import { createHash } from 'crypto';

/**
 * Accepted output formats.
 */
export type OutputFormat = 'webp' | 'jpeg' | 'png' | 'avif';

/**
 * Options that control the compression / resizing.
 */
export interface ImageProcessingOptions {
  /** Desired width (px). If omitted, height alone is used. */
  width?: number;
  /** Desired height (px). If omitted, width alone is used. */
  height?: number;
  /** Output quality (0‑100 for lossy formats, 0‑9 for PNG). */
  quality?: number;
  /** Desired output format. If omitted the source format is preserved. */
  format?: OutputFormat;
  /** How to fit the image into the target box. */
  fit?: keyof typeof sharp.fit; // e.g. 'cover' | 'inside' | 'contain' …
}

/**
 * Result of a successful compression.
 */
export interface CompressedImage {
  /** Raw buffer – useful for streaming directly to a response. */
  buffer: Buffer;
  /** Base64 representation (without data‑uri prefix). */
  base64: string;
  /** MIME type that matches the produced image. */
  mime: string;
}

/**
 * Small utility – strip a possible data‑uri prefix.
 * Returns the clean base64 part.
 */
function stripDataUriPrefix(base64: string): string {
  const match = base64.match(/^data:.*?;base64,(.*)$/);
  return match ? match[1] : base64;
}

/**
 * Small utility – turn a format string into a MIME type.
 */
function mimeFromFormat(format: OutputFormat): string {
  const map: Record<OutputFormat, string> = {
    webp: 'image/webp',
    jpeg: 'image/jpeg',
    png: 'image/png',
    avif: 'image/avif',
  };
  return map[format];
}

/**
 * Core function – convert a Base64 image into a (possibly) resized,
 * re‑encoded Buffer. All heavy lifting is done here.
 *
 * @throws on malformed input or on Sharp failure.
 */
export async function compressBase64ToBuffer(
  base64Image: string,
  opts: ImageProcessingOptions = {}
): Promise<CompressedImage> {
  // -----------------------------------------------------------------
  // 1️⃣  Normalise input
  // -----------------------------------------------------------------
  const cleanBase64 = stripDataUriPrefix(base64Image);
  const srcBuffer = Buffer.from(cleanBase64, 'base64');

  // -----------------------------------------------------------------
  // 2️⃣  Determine output format & quality defaults
  // -----------------------------------------------------------------
  const srcMetadata = await sharp(srcBuffer).metadata(); // cheap, caches info
  const format: OutputFormat = opts.format ?? (srcMetadata.format as OutputFormat) ?? 'jpeg';

  const quality = opts.quality ?? (() => {
    switch (format) {
      case 'webp':
      case 'jpeg':
      case 'avif':
        return 8;
      case 'png':
        return 9; // PNG compression level (0‑9)
    }
  })();

  // -----------------------------------------------------------------
  // 3️⃣  Build Sharp pipeline
  // -----------------------------------------------------------------
  let pipeline: Sharp = sharp(srcBuffer)
    .rotate() // auto‑apply EXIF orientation
    .withMetadata({ orientation: 1 }); // strip all other metadata

  // Only resize when we have something to resize to.
  if (opts.width !== undefined || opts.height !== undefined) {
    pipeline = pipeline.resize(opts.width, opts.height, {
      fit: opts.fit ?? 'cover', // default to cover for thumbnails
      position: sharp.strategy.entropy, // better visual crop
    });
  }

  // Choose the right output method
  switch (format) {
    case 'webp':
      pipeline = pipeline.webp({ quality });
      break;
    case 'jpeg':
      pipeline = pipeline.jpeg({ quality, mozjpeg: true });
      break;
    case 'png':
      pipeline = pipeline.png({ compressionLevel: quality as number });
      break;
    case 'avif':
      pipeline = pipeline.avif({ quality });
      break;
  }

  const outBuffer = await pipeline.toBuffer();

  return {
    buffer: outBuffer,
    base64: outBuffer.toString('base64'),
    mime: mimeFromFormat(format),
  };
}

/**
 * Convenience wrapper that returns a **data‑uri** ready string.
 */
export async function compressBase64ToDataUri(
  base64Image: string,
  opts: ImageProcessingOptions = {}
): Promise<string> {
  const { base64, mime } = await compressBase64ToBuffer(base64Image, opts);
  return `data:${mime};base64,${base64}`;
}

/* -----------------------------------------------------------------------
 *  Cache layer – LRU in‑memory (replace with Redis for multi‑node)
 * ---------------------------------------------------------------------*/

export interface AvatarCacheValue {
  /** Thumbnail data‑uri (already prefixed). */
  avatarThumbnail: string | null;
  /** Medium‑size data‑uri. */
  avatarMedium: string | null;
}

/**
 * Simple LRU wrapper. The default max size is 5000 entries (~few hundred MB)
 * which you can tune via env vars.
 */
class AvatarCache {
  private cache: LRUCache<string, AvatarCacheValue>;

  constructor() {
    this.cache = new LRUCache<string, AvatarCacheValue>({
      max: Number(5_000),
      ttl: Number(60 * 60 * 1000), // 1h
    });
  }

  /** Deterministic cache key based on assistant id + avatar hash. */
  private makeKey(assistantId: string, avatarBase64: string): string {
    // Use a hash to keep the key length short even if the base64 string is huge.
    const hash = createHash('sha1').update(avatarBase64).digest('hex');
    return `assistant:${assistantId}:avatar:${hash}`;
  }

  get(assistantId: string, avatarBase64: string): AvatarCacheValue | undefined {
    return this.cache.get(this.makeKey(assistantId, avatarBase64));
  }

  set(assistantId: string, avatarBase64: string, value: AvatarCacheValue): void {
    this.cache.set(this.makeKey(assistantId, avatarBase64), value);
  }

  /** Expose the underlying LRU for stats / debugging (optional). */
  // stats() {
  //   return this.cache.stats;
  // }
}

export const avatarCache = new AvatarCache();

/* -----------------------------------------------------------------------
 *  Public API – assistant avatar processing
 * ---------------------------------------------------------------------*/

export interface Assistant {
  id: string;
  meta: {
    avatar_base64?: string | null;
  };
}

/**
 * Returns an object that contains ready‑to‑use data‑uri strings for the
 * thumbnail (80×80 webp) and the medium version (300×300 jpeg by default).
 *
 * The result is cached per‑assistant + avatar hash.
 */
export async function processAssistantAvatars(
  assistant: Assistant
): Promise<AvatarCacheValue> {
  const rawBase64 = assistant.meta.avatar_base64;
  if (!rawBase64) {
    return { avatarThumbnail: null, avatarMedium: null };
  }

  // -----------------------------------------------------------------
  // 1️⃣  Cache lookup
  // -----------------------------------------------------------------
  const cached = avatarCache.get(assistant.id, rawBase64);
  if (cached) {
    return cached;
  }

  // -----------------------------------------------------------------
  // 2️⃣ Generate both sizes (run in parallel)
  // -----------------------------------------------------------------
  const [thumb, medium] = await Promise.all([
    compressBase64ToDataUri(rawBase64, {
      width: 300,
      height: 300,
      format: 'webp',
      quality: 7,
      fit: 'cover',
    }),
    compressBase64ToDataUri(rawBase64, {
      width: 300,
      height: 300,
      // keep original format for medium; fallback is jpeg
      quality: 8,
      fit: 'inside',
    }),
  ]);

  const result: AvatarCacheValue = {
    avatarThumbnail: thumb,
    avatarMedium: medium,
  };

  avatarCache.set(assistant.id, rawBase64, result);
  return result;
}
