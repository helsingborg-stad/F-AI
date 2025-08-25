<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'

  const { Story } = defineMeta({
    title: 'Components/Divider/Horizontal',
    component: HorizontalDivider,
    tags: ['autodocs'],
  })
</script>

<Story name="Default">
  <p>Some text before divider</p>
  <HorizontalDivider />
  <p>Some text after divider</p>
</Story>
