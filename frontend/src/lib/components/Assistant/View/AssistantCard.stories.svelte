<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantCard from '$lib/components/Assistant/View/AssistantCard.svelte'
  import { mockAssistantCards } from '$lib/components/Assistant/View/storiesMockData.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/View/AssistantCard',
    component: AssistantCard,
    tags: ['autodocs'],
  })
</script>

<Story
  name="Default"
  args={mockAssistantCards[0]}
/>