<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ColorPicker from '$lib/components/ColorPicker/ColorPicker.svelte'

  const { Story } = defineMeta({
    title: 'Components/ColorPicker',
    component: ColorPicker,
    tags: ['autodocs'],
    argTypes: {
      selectedColor: {
        control: { type: 'select' },
        options: [
          'transparent',
          '#e28a8a',
          '#d88bb8',
          '#b18be0',
          '#8ba6e0',
          '#8bd0c6',
          '#9dd990',
          '#f0d27a',
          '#e0bd91',
        ],
        description: 'The currently selected color.',
      },
      colors: {
        control: { type: 'object' },
        description: 'Array of available colors to choose from.',
      },
      onColorSelect: {
        action: 'colorSelected',
        description: 'Callback function triggered when a color is selected.',
      },
    },
  })
</script>

<Story
  name="Default"
  args={{
    selectedColor: 'transparent'
  }}
/>

<Story
  name="With Color Selected"
  args={{
    selectedColor: '#e28a8a'
  }}
/>

<Story
  name="Custom Colors"
  args={{
    selectedColor: '#ff0000',
    colors: ['transparent', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#800080']
  }}
/>

<Story
  name="Transparent Selected"
  args={{
    selectedColor: 'transparent'
  }}
/>
