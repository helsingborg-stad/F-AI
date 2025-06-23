<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import WebSearch from '$lib/components/Buttons/WebSearch.svelte'

  interface Props {
    allowSearch: boolean
    assistants: IAssistantMenu[],
    selectedAssistantId: string,
    disableAssistantPicker: boolean
  }

  let {
    allowSearch,
    assistants,
    selectedAssistantId = $bindable(),
    disableAssistantPicker,
  }: Props = $props()
</script>

<div class="flex flex-row pr-3 gap-1">
  {#if allowSearch}
    <WebSearch />
  {/if}
  <div class="ml-auto">
    <AssistantPicker
      {assistants}
      disabled={disableAssistantPicker}
      bind:selectedAssistantId
    />
  </div>
</div>
