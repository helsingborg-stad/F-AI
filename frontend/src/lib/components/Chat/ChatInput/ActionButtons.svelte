<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import WebSearch from '$lib/components/Buttons/WebSearch.svelte'

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

<div class="flex flex-row pr-3 gap-1">
  <WebSearch />
  <div class="ml-auto">
    <AssistantPicker
      {assistants}
      disabled={disableAssistantPicker}
      bind:selectedAssistantId
    />
  </div>
</div>
