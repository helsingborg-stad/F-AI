<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantSignSummery from '$lib/components/Assistant/View/Sign/AssistantSignSummery.svelte'
  import { mockAssistantCards } from '$lib/components/Assistant/View/storiesMockData.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/View/AssistantSignSummery',
    component: AssistantSignSummery,
    tags: ['autodocs'],
  })
</script>

<Story
  name="Default"
  args={{...mockAssistantCards[0]}}
/>
