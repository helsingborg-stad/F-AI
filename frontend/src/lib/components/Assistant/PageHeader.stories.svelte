<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import PageHeader from '$lib/components/Assistant/PageHeader.svelte'

  const { Story } = defineMeta({
    title: 'Components/Assistant/PageHeader',
    component: PageHeader,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" />

<Story name="With create enabled" args={{ canCreateAssistant: true }} />
