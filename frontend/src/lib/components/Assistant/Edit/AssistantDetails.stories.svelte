<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantDetails from '$lib/components/Assistant/Edit/AssistantDetails.svelte'
  import { mockAssistants } from '$lib/mock/assistants.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/Details',
    component: AssistantDetails,
    tags: ['autodocs'],
  })

  const newAssistant = {
    id: '6808ddaffcd3461eea42133f',
  }
</script>

<Story name="Default" />

<Story name="Create new assistant" args={{ assistant: newAssistant, canEdit: true }} />

<Story name="With assistant and 'can edit' enabled" args={{ assistant: mockAssistants[0], canEdit: true }} />

<Story name="With assistant and 'can edit' disabled" args={{ assistant: mockAssistants[0], canEdit: false }} />
