<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ActionButtons from '$lib/components/Chat/ChatInput/ActionButtons.svelte'

  const { Story } = defineMeta({
    title: 'Components/Chat/ActionButtons',
    component: ActionButtons,
    parameters: {
      layout: 'centered', // This will center the component
    },
  })
</script>

<Story name="Default" args={{
  assistants: [
    {id: '0', name: 'Language assistant'},
    {id: '1', name: 'Math assistant'},
    ]
}}
/>