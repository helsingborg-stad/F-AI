<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantDetails from '$lib/components/assistant/AssistantDetails.svelte'
  import type { IAssistant } from '$lib/types.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/Details',
    component: AssistantDetails,
    tags: ['autodocs'],
  })

  const assistant: IAssistant = {
    id: '6808ddaffcd3461eea42133f',
    owner: 'user@example.com',
    name: 'Research Assistant',
    description: 'Helps with research tasks and information gathering',
    instructions: 'Answer questions clearly and cite sources when possible',
    model: 'gpt-4',
  }
</script>

<Story name="Default" />

<Story name="With assistant" args={{ assistant }} />