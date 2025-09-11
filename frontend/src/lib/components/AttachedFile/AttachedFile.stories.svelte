<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AttachedFile from '$lib/components/AttachedFile/AttachedFile.svelte'

  const { Story } = defineMeta({
    title: 'Components/AttachedFile',
    component: AttachedFile,
    tags: ['autodocs'],
  })
</script>
<script>
import { fn } from '@storybook/test'
</script>

<Story name='default' args={{
  title: 'MyFile.txt',
  onRemove: fn(),
  state: 'valid'
}} />
