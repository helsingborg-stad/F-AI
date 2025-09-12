<script lang="ts">
  import { MODEL_COLORS, DEFAULT_MODEL_COLOR } from '$lib/constants/colors.js'

  interface Props {
    selectedColor?: string
    colors?: string[]
    onColorSelect?: (color: string) => void
  }

  let {
    selectedColor = DEFAULT_MODEL_COLOR,
    colors = MODEL_COLORS,
    onColorSelect = () => {}
  }: Props = $props()

  function selectColor(color: string) {
    onColorSelect(color)
  }
</script>

<div class="ml-1 mt-3 flex">
  {#each colors as color, i}
    <button
      type="button"
      class="relative ml-[-8px] h-10 w-10 cursor-pointer overflow-hidden rounded-full outline outline-white transition-all first:ml-0 hover:z-10 hover:scale-110"
      style="{color === 'transparent'
        ? 'background: repeating-linear-gradient(45deg, #e5e5e5, #e5e5e5 5px, white 5px, white 10px);'
        : `background-color: ${color};`}
              {selectedColor === color
        ? 'border: 2px solid white; outline: 2px solid gold; z-index: 5;'
        : ''}"
      onclick={() => selectColor(color)}
      aria-label={`Select ${color === 'transparent' ? 'transparent' : `color ${i}`}`}
      aria-pressed={selectedColor === color}
    >
      {#if color === 'transparent'}
        <span class="sr-only">Transparent</span>
      {/if}
    </button>
  {/each}
</div>
