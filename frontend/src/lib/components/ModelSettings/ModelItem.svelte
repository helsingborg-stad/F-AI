<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import CapabilityBadges from './CapabilityBadges.svelte'

  interface Props {
    model: IAssistantModel
    canEdit?: boolean
    canDelete?: boolean
    onEdit?: (model: IAssistantModel) => void
    onDelete?: (model: IAssistantModel) => void
  }

  let {
    model,
    canEdit = false,
    canDelete = false,
    onEdit,
    onDelete,
  }: Props = $props()

  function handleEdit() {
    if (onEdit) onEdit(model)
  }

  function handleDelete() {
    if (onDelete) onDelete(model)
  }
</script>

<div class="flex items-center justify-between px-6 py-4">
  <div class="flex-1">
    <div class="flex items-center space-x-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-base-200">
        <span class="text-xs font-medium text-base-content/70">
          {model.provider.substring(0, 2).toUpperCase()}
        </span>
      </div>
      <div>
        <h3 class="text-sm font-medium text-base-content">
          {model.display_name || model.name}
        </h3>
        <p class="text-xs text-base-content/60">{model.key}</p>
        <p class="text-xs text-base-content/70">{model.provider}</p>
        {#if model.meta?.description}
          <p class="mt-1 text-xs text-base-content/60">{model.meta.description}</p>
        {/if}
        <CapabilityBadges capabilities={model.meta?.capabilities} />
      </div>
    </div>
  </div>

  <div class="flex items-center space-x-2">
    {#if canEdit}
      <button
        type="button"
        class="btn btn-ghost btn-sm"
        onclick={handleEdit}
      >
        <span class="text-xs">Edit</span>
      </button>
    {/if}
    {#if canDelete}
      <button
        type="button"
        class="btn btn-ghost btn-sm text-error"
        onclick={handleDelete}
      >
        <span class="text-xs">Delete</span>
      </button>
    {/if}
  </div>
</div>