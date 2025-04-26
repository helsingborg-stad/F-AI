<script lang="ts">
  import PageHeader from '$lib/components/assistant/PageHeader.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'
  import AssistantTable from '$lib/components/assistant/AssistantTable.svelte'
  import type { IAssistant } from '$lib/types.js'

  interface Props {
    canCreateAssistant?: boolean
    assistants?: IAssistant[]
  }

  let { canCreateAssistant = false, assistants = [] }: Props = $props()
</script>

<div class="flex flex-col min-h-0 h-full">
  <PageHeader title="Assistants" {canCreateAssistant} />
  <HorizontalDivider />
  <div class="flex w-full justify-center flex-1 gap-4">
    <div class="flex-1">
      <AssistantTable {assistants}/>
    </div>
    <VerticalDivider />
    <div class="flex-1">
      <p>Assistant details</p>
    </div>
  </div>
</div>