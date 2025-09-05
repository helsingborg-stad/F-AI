<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModelAvatar from './ModelAvatar.svelte'
  import ModelHeader from './ModelHeader.svelte'
  import ModelCapabilities from './ModelCapabilities.svelte'
  import ModelTechnicalDetails from './ModelTechnicalDetails.svelte'

  interface Props {
    model: IAssistantModel
    index: number
    selectedKey: string | null
    canEdit: boolean
    name: string
    onSelection: (modelKey: string) => void
  }

  let { model, index, selectedKey, canEdit, name, onSelection }: Props = $props()

  const isSelected = $derived(selectedKey === model.key)
  const modelId = $derived(`${name}-model-${index}`)

  function handleSelection() {
    if (!canEdit) return
    onSelection(model.key)
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (!canEdit) return

    if (event.key === ' ' || event.key === 'Enter') {
      event.preventDefault()
      handleSelection()
    }
  }

  function getModelAriaLabel(): string {
    const status = isSelected ? 'selected' : 'not selected'
    return `${model.displayName} by ${model.provider}, ${status}. ${model.enhancedDescription}`
  }
</script>

<div
  class="card collapse collapse-plus relative
         {isSelected
    ? 'border-2 border-primary bg-primary/5 shadow-md'
    : 'border border-base-300 bg-base-200 hover:bg-base-300/50 hover:shadow-sm'}"
  class:cursor-not-allowed={!canEdit}
  class:opacity-60={!canEdit}
  class:cursor-pointer={canEdit}
  class:selected={isSelected}
  class:disabled={!canEdit}
>
  <input
    type="radio"
    id={modelId}
    name="model-accordion-{name}"
    value={model.key}
    checked={isSelected}
    disabled={!canEdit}
    onchange={handleSelection}
    class="absolute top-4 right-4 z-10"
  />

  <div
    role="radio"
    tabindex={canEdit ? 0 : -1}
    aria-checked={isSelected}
    aria-label={getModelAriaLabel()}
    aria-describedby="{modelId}-description"
    onkeydown={handleKeyDown}
    onclick={handleSelection}
  >
    <label
      for={modelId}
      class="collapse-title card-body p-4"
    >
      <div class="flex items-start gap-4">
        <div class="mt-1">
          <ModelAvatar
            avatar={model.meta?.avatar_base64}
            provider={model.provider}
            primaryColor={model.meta?.primaryColor || 'transparent'}
            {isSelected}
          />
        </div>

        <div class="min-w-0 flex-1">
          <ModelHeader model={model} {isSelected} />

          <p class="line-clamp-2 text-sm leading-relaxed text-base-content/80">
            {model.enhancedDescription}
          </p>

          <p class="mt-1 truncate font-mono text-xs text-base-content/60">
            {model.key}
          </p>
        </div>
      </div>
    </label>
  </div>

  <div class="collapse-content">
    <div class="card-body pt-0" id="{modelId}-description">
      <ModelCapabilities capabilities={model.meta?.capabilities} />

      <ModelTechnicalDetails
        modelKey={model.key}
        provider={model.provider}
      />
    </div>
  </div>
</div>
