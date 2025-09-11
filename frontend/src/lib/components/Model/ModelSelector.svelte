<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModelSelectorModal from './ModelSelectorModal/ModelSelectorModal.svelte'
  import ModelAvatar from './ModelAccordion/ModelAvatar.svelte'
  import Badge from '$lib/components/Badge/Badge.svelte'

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

  let modalRef: ModelSelectorModal

  const selectedModel = $derived.by(() =>
    selectedKey ? models.find((m) => m.key === selectedKey) : null
  )

  const placeholderModel = $derived.by(() =>
    models.length > 0 ? models[0] : null
  )

  function openModal() {
    if (!canEdit) return
    modalRef?.showModal()
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (!canEdit) return
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      openModal()
    }
  }

  function handleSelection(modelKey: string) {
    selectedKey = modelKey
    if (onSelection) {
      onSelection(modelKey)
    }
  }
</script>

<input type="hidden" {name} value={selectedKey || ''} />

<div class="model-selector">
  <button
    type="button"
    class="w-full rounded-lg border-2 border-base-300 bg-base-100 p-4 text-left"
    onclick={openModal}
    onkeydown={handleKeyDown}
    disabled={!canEdit}
    aria-label="Select AI model"
    aria-haspopup="dialog"
    aria-expanded="false"
  >
    {#if selectedModel || placeholderModel}
      {@const model = selectedModel || placeholderModel}
      {@const isPlaceholder = !selectedModel}

      {#if model}
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="{isPlaceholder ? 'opacity-50' : ''}">
              <ModelAvatar
                avatar={model.meta?.avatar_base64}
                provider={model.provider}
                primaryColor={model.meta?.primaryColor || 'transparent'}
                isSelected={false}
                size="sm"
              />
            </div>

            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="text-sm font-semibold text-base-content {isPlaceholder ? 'opacity-50' : ''}">
                  {isPlaceholder ? 'Select a model' : model.displayName}
                </h3>
                {#if !isPlaceholder}
                  <Badge type="provider" size="sm" variant="outline" label={model.provider} />
                  {#if model.meta?.capabilities?.supportsImagegen}
                    <Badge type="image" size="sm" />
                  {/if}
                  {#if model.meta?.capabilities?.supportsReasoning}
                    <Badge type="reasoning" size="sm" />
                  {/if}
                  {#if model.meta?.capabilities?.supportsWebSearch}
                    <Badge type="web-search" size="sm" />
                  {/if}
                {/if}
              </div>
              {#if !isPlaceholder}
                <p class="mt-1 text-xs text-base-content/60 line-clamp-1 overflow-hidden">
                  {model.enhancedDescription}
                </p>
              {/if}
            </div>
          </div>

          <div class="flex-shrink-0">
            <svg
              class="h-5 w-5 text-base-content/50"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </div>
        </div>
      {/if}
    {:else}

      <div class="flex items-center justify-between">
        <span class="text-base-content/50">No models available</span>
        <svg
          class="h-5 w-5 text-base-content/30"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          ></path>
        </svg>
      </div>
    {/if}
  </button>
</div>

<ModelSelectorModal
  bind:this={modalRef}
  {models}
  {selectedKey}
  {canEdit}
  onSelection={handleSelection}
/>
