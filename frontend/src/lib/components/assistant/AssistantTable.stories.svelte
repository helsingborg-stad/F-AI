<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantTable from '$lib/components/assistant/AssistantTable.svelte'
  import { mockAssistants } from '../../../stories/data/assistants.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/Table',
    component: AssistantTable,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" />

<Story name="With assistants" args={{ assistants: mockAssistants }} />

<Story name="With active assistant"
       args={{ assistants: mockAssistants, activeAssistantId: '6651afc3a7b5e3c8d9f01234' }} />