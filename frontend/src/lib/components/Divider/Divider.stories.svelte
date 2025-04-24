<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Divider from '$lib/components/Divider/Divider.svelte'

  const { Story } = defineMeta({
    title: 'Components/Divider',
    component: Divider,
    tags: ['autodocs'],
  })
</script>

<Story name="Default">
  <p>Some text before divider</p>
  <Divider />
  <p>Some text after divider</p>
</Story>

<Story name="Vertical">
  <div class="flex h-24 items-center">
    <span>Left content</span>
    <Divider vertical={true} width="1" />
    <span>Right content</span>
  </div>
</Story>