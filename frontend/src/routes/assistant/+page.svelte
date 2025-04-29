<script lang="ts">
  import type { IAssistant } from '$lib/types.js'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import PageHeader from '$lib/components/assistant/PageHeader.svelte'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'
  import MainPage from '$lib/components/assistant/MainPage.svelte'

  let { data } = $props<{ assistants: IAssistant[] }>()

  const assistants = data.assistants
  const canCreateAssistant = data.canCreateAssistant
  const activeAssistant = data.activeAssistant
  const canEditActiveAssistant = data.canEditActiveAssistant
</script>

<MainPage {canCreateAssistant} {assistants} {activeAssistant} {canEditActiveAssistant} />