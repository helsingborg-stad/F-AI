<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import IconToggleButton from '$lib/components/Buttons/IconToggleButton.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  const { Story } = defineMeta({
    title: 'Components/Buttons/IconToggleButton',
    component: IconToggleButton,
    tags: ['autodocs'],
  })
</script>

<Story name="default" args={{ icon: icons.save, title: 'Title' }} />
