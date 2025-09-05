const MODEL_COLORS_TUPLE = [
  'transparent',
  '#e28a8a',
  '#d88bb8',
  '#b18be0',
  '#8ba6e0',
  '#8bd0c6',
  '#9dd990',
  '#f0d27a',
  '#e0bd91',
] as const

// Mutable copy for components that expect string[]
export const MODEL_COLORS = [...MODEL_COLORS_TUPLE]

export const DEFAULT_MODEL_COLOR = 'transparent'

export type ModelColor = typeof MODEL_COLORS_TUPLE[number]

export function getRandomModelColor(): ModelColor {
  const colorOptions = MODEL_COLORS_TUPLE.filter(color => color !== 'transparent')
  return colorOptions[Math.floor(Math.random() * colorOptions.length)]
}

export function isValidModelColor(color: string): color is ModelColor {
  return MODEL_COLORS_TUPLE.includes(color as ModelColor)
}
