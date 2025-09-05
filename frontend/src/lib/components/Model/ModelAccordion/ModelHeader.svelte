<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import Badge from '$lib/components/Badge/Badge.svelte'

  interface Props {
    model: IAssistantModel
    isSelected: boolean
  }

  let { model, isSelected }: Props = $props()
</script>

<div class="mb-2 flex items-start justify-between gap-3">
  <div class="min-w-0 flex-1">
    <h3 class="truncate text-base font-semibold leading-snug text-base-content">
      {model.displayName}
    </h3>
    <div class="mt-1 flex items-center gap-2">
      <Badge type="provider" size="sm" variant="outline" label={model.provider} {isSelected} />
      {#if model.meta?.capabilities?.supportsImages}
        <Badge type="image" size="sm" />
      {/if}
      {#if model.meta?.capabilities?.supportsReasoning}
        <Badge type="reasoning" size="sm" />
      {/if}
    </div>
  </div>

  <div class="flex-shrink-0">
    <input
      type="radio"
      class="radio radio-primary"
      checked={isSelected}
      disabled
      aria-hidden="true"
    />
  </div>
</div>
