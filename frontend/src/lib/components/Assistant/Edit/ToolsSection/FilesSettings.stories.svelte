<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import FilesSettings from '$lib/components/Assistant/Edit/ToolsSection/FilesSettings.svelte'

  const { Story } = defineMeta({
    title: 'Components/Assistant/Details/FileSettings',
    component: FilesSettings,
    tags: ['autodocs'],
    parameters: {
      layout: 'centered',
    }
  })
</script>

<Story name="Default" />
