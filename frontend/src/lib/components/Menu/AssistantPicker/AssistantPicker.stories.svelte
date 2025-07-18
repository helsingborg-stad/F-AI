<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import {
    mockOnlyAssistants,
    mockTitleAndAssistants,
    mockWithHiddenAssistants,
  } from '$stories/assets/mockData/assistantPicker.ts'

  const { Story } = defineMeta({
    title: 'Components/Menu/AssistantPicker',
    component: AssistantPicker,
    parameters: {
      layout: 'centered',
    },
  })
</script>

<Story name="Default" />

<Story name="With no titles" args={{assistants: mockOnlyAssistants}} />

<Story name="With title and assistants" args={{assistants: mockTitleAndAssistants}} />

<Story name="With hidden assistants" args={{assistants: mockWithHiddenAssistants}} />
