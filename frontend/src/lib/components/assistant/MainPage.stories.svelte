<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import MainPage from '$lib/components/assistant/MainPage.svelte'
  import { mockAssistants } from '../../../stories/data/assistants.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/MainPage',
    component: MainPage,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" />

<Story name="With assistants" args={{ assistants: mockAssistants }} />