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

<Story
  name="With primary color and no avatar'"
  args={{...mockAssistantCards[2]}}
/>

<Story
  name="With transparent color and no avatar'"
  args={{...mockAssistantCards[3]}}
/>
