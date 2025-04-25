<script lang="ts">
  import type { IAssistant } from '$lib/types.js'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import PageHeader from '$lib/components/assistant/PageHeader.svelte'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'

  let { data } = $props<{ assistants: IAssistant[] }>()

  const assistants = data.assistants
  const enableCreate = true
</script>

<div class="flex flex-col min-h-0 h-full">
  <PageHeader title="Assistants" {enableCreate} />
  <HorizontalDivider />
  <div class="flex flex-1 gap-4">
    <p>List of assistants</p>
    <VerticalDivider />
    <p>Assistant details</p>
  </div>
</div>

