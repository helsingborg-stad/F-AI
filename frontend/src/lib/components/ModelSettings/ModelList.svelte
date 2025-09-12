<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModelItem from './ModelItem.svelte'

  interface Props {
    models: IAssistantModel[]
    canEdit?: boolean
    canDelete?: boolean
    onEditModel?: (model: IAssistantModel) => void
    onDeleteModel?: (model: IAssistantModel) => void
  }

  let {
    models = [],
    canEdit = false,
    canDelete = false,
    onEditModel,
    onDeleteModel,
  }: Props = $props()
</script>

<div class="rounded-lg bg-white shadow">
  <div class="border-b border-base-300 px-6 py-4">
    <h2 class="text-lg font-semibold text-base-content">Available Models</h2>
    <p class="text-sm text-base-content/70">Currently configured AI models</p>
  </div>

  <div class="divide-y divide-base-300">
    {#each models as model (model.key)}
      <ModelItem
        {model}
        {canEdit}
        {canDelete}
        onEdit={onEditModel}
        onDelete={onDeleteModel}
      />
    {/each}

    {#if models.length === 0}
      <div class="px-6 py-8 text-center">
        <p class="text-base-content/60">No models available</p>
      </div>
    {/if}
  </div>
</div>
