<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import IconToggleButton from '$lib/components/Buttons/IconToggleButton.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    allowSearch: boolean
    allowReasoning: boolean
    enableSearch: boolean
    enableReasoning: boolean
    assistants: IAssistantMenu[],
    selectedAssistantId: string,
    disableAssistantPicker: boolean
  }

  let {
    allowSearch,
    allowReasoning,
    enableSearch = $bindable(),
    enableReasoning = $bindable(),
    assistants,
    selectedAssistantId = $bindable(),
    disableAssistantPicker,
  }: Props = $props()
</script>

<div class="flex flex-row pr-3 gap-1">
  {#if allowSearch}
    <IconToggleButton title="Web search" icon={icons['globe']} bind:value={enableSearch} />
  {/if}
  {#if allowReasoning}
    <IconToggleButton title="Reasoning" icon={icons['globe']} bind:value={enableReasoning} />
  {/if}
  <div class="ml-auto">
    <AssistantPicker
      {assistants}
      disabled={disableAssistantPicker}
      bind:selectedAssistantId
    />
  </div>
</div>
