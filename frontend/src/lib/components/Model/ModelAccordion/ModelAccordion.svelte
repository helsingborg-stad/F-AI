<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModelItem from './ModelItem.svelte'
  import EmptyState from './EmptyState.svelte'

  interface Props {
    models: IAssistantModel[]
    selectedKey: string | null
    canEdit: boolean
    name?: string
    onSelection?: (modelKey: string) => void
  }

  let {
    models = [],
    selectedKey = $bindable(null),
    canEdit = true,
    name = 'model',
    onSelection,
  }: Props = $props()

  function handleSelection(modelKey: string) {
    if (!canEdit) return

    selectedKey = modelKey

    if (onSelection) {
      onSelection(modelKey)
    }
  }
</script>

<input type="hidden" {name} value={selectedKey ?? ''} />

<div
  class="model-accordion space-y-3"
  role="radiogroup"
  aria-label="Select AI model"
  aria-describedby="{name}-help"
>
  {#each models as model, index}
    <ModelItem
      {model}
      {index}
      {selectedKey}
      {canEdit}
      {name}
      onSelection={handleSelection}
    />
  {/each}

  {#if models.length === 0}
    <EmptyState />
  {/if}
</div>
