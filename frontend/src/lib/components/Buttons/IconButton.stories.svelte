<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import IconButton from '$lib/components/Buttons/IconButton.svelte'
  import { fn } from '@storybook/test'
  import { icons } from '$lib/components/Icon/icons.js'

  const { Story } = defineMeta({
    title: 'Components/Buttons/IconButton',
    component: IconButton,
    tags: ['autodocs'],
  })
</script>

<Story name="default" args={{ icon: icons.save, onClick: fn(), tooltip: 'Tooltip' }} />
