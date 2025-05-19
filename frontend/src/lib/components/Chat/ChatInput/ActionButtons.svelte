<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'

  interface Props {
    assistants: {
      id: string,
      name: string,
    }[],
    selectedAssistantId: string,
  }

  let { assistants, selectedAssistantId = $bindable() }: Props = $props()
</script>

<div class="flex flex-row px-3 gap-1 justify-end">
  <AssistantPicker {assistants} bind:selectedAssistantId={selectedAssistantId} />
</div>