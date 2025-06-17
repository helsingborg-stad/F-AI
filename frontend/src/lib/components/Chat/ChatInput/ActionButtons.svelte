<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'

  interface Props {
    assistants: IAssistantMenu[],
    selectedAssistantId: string,
    disableAssistantPicker: boolean
  }

  let {
    assistants,
    selectedAssistantId = $bindable(),
    disableAssistantPicker,
  }: Props = $props()
</script>

<div class="flex flex-row px-3 gap-1 justify-end">
  <AssistantPicker
    {assistants}
    disabled={disableAssistantPicker}
    bind:selectedAssistantId
  />
</div>
