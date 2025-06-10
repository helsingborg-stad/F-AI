<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantSign from '$lib/components/Assistant/View/Sign/AssistantSign.svelte'
  import { mockAssistantCards } from '$lib/components/Assistant/View/storiesMockData.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/View/AssistantSign',
    component: AssistantSign,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={{
  ...mockAssistantCards[0],
}} />
