<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'

  const { Story } = defineMeta({
    title: 'Components/Divider/Vertical',
    component: VerticalDivider,
    tags: ['autodocs'],
  })
</script>

<Story name="Default">
  <div class="flex items-center h-32 gap-4">
    <p>Left content</p>
    <VerticalDivider />
    <p>Right content</p>
  </div>
</Story>
