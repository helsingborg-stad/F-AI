<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModelAccordion from '../ModelAccordion/ModelAccordion.svelte'

  interface Props {
    models: IAssistantModel[]
    selectedKey: string | null
    canEdit: boolean
  }

  let {
    models = [],
    selectedKey = $bindable(),
    canEdit = true
  }: Props = $props()
</script>

<div class="flex-1 overflow-y-auto pr-2">
  <ModelAccordion
    {models}
    bind:selectedKey
    {canEdit}
    name="modal-model"
  />
</div>
