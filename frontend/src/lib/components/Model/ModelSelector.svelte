<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import { getEnhancedModelInfo } from '$lib/utils/modelHelpers.js'
  import ModelSelectorModal from './ModelSelectorModal/ModelSelectorModal.svelte'
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

  const selectedModel = $derived(
    selectedKey && models.find((m) => m.key === selectedKey) 
      ? getEnhancedModelInfo(models.find((m) => m.key === selectedKey)!) 
      : null
  )

  const placeholderModel = $derived(
    models.length > 0 ? getEnhancedModelInfo(models[0]) : null
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
    class="w-full rounded-lg border-2 border-base-300 bg-base-100 p-4 text-left transition-all duration-200 hover:-translate-y-px hover:border-primary hover:bg-base-200 hover:shadow-md focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 disabled:hover:border-base-300 disabled:hover:bg-base-100 disabled:hover:shadow-none"
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
          <!-- Model Info Section -->
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="avatar flex-shrink-0">
              <div class="h-10 w-10 rounded-lg shadow-sm {isPlaceholder ? 'opacity-50' : ''}">
                {#if model.avatar}
                  <img
                    src={model.avatar}
                    alt=""
                    class="h-full w-full rounded-lg object-cover"
                    role="presentation"
                  />
                {:else}
                  <div
                    class="flex h-full w-full items-center justify-center rounded-lg text-xs font-semibold text-white shadow-inner"
                    style="background-color: {model.primaryColor}"
                    role="presentation"
                  >
                    {model.provider.substring(0, 2).toUpperCase()}
                  </div>
                {/if}
              </div>
            </div>

            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="text-sm font-semibold text-base-content {isPlaceholder ? 'opacity-50' : ''}">
                  {isPlaceholder ? 'Select a model' : model.displayName}
                </h3>
                {#if !isPlaceholder}
                  <Badge type="provider" size="sm" variant="outline" label={model.provider} />
                  {#if model.meta?.capabilities?.supportsImages}
                    <Badge type="image" size="xs" />
                  {/if}
                  {#if model.meta?.capabilities?.supportsReasoning}
                    <Badge type="reasoning" size="xs" />
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
