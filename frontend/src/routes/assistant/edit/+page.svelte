<script lang="ts">
  import type { IAssistant, IAssistantModel } from '$lib/types.js'
  import MainPage from '$lib/components/assistant/MainPage.svelte'

  let { data } = $props<{ assistants: IAssistant[], models: IAssistantModel[] }>()

  const assistants = data.assistants
  const activeAssistant = data.activeAssistant
  const models = data.models
  const canCreateAssistant = data.canCreateAssistant
  const canEditActiveAssistant = data.canEditActiveAssistant
</script>

<MainPage
  {assistants}
  {activeAssistant}
  {models}
  {canCreateAssistant}
  {canEditActiveAssistant}
/>
