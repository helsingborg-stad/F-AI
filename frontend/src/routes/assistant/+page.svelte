<script lang="ts">
  import type { IAssistant } from '$lib/types.js'
  import Divider from '$lib/components/Divider/Divider.svelte'
  import PageHeader from '$lib/components/assistant/PageHeader.svelte'

  let { data } = $props<{ assistants: IAssistant[] }>()

  const assistants = data.assistants
  const nrOfAssistants = assistants.length
  const enableCreate = true
</script>

<PageHeader title="Assistants" {enableCreate} />
<Divider />
<div class="flex w-full">
  <p>List of assistants</p>
  <Divider />
  <p>Assistant details</p>
</div>

