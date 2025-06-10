<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ActionButtons from '$lib/components/Chat/ChatInput/ActionButtons.svelte'
  import { mockOnlyAssistants } from '$stories/assets/mockData/assistantPicker.ts'

  const { Story } = defineMeta({
    title: 'Components/Chat/ActionButtons',
    component: ActionButtons,
    parameters: {
      layout: 'centered',
    },
  })
</script>

<Story name="Default" args={{ assistants: mockOnlyAssistants }}
/>
