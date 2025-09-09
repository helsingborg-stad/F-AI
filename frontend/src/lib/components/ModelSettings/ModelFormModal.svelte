<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import { enhance, applyAction } from '$app/forms'
  import { invalidateAll } from '$app/navigation'
  import CapabilitiesSection from './CapabilitiesSection.svelte'
  import ColorPicker from '../ColorPicker/ColorPicker.svelte'
  import { getRandomModelColor, DEFAULT_MODEL_COLOR } from '$lib/constants/colors.js'
  import X from 'lucide-svelte/icons/x'

  interface Props {
    isOpen: boolean
    mode: 'create' | 'edit'
    model?: IAssistantModel | null
    onClose: () => void
  }

  let { isOpen = false, mode = 'create', model = null, onClose }: Props = $props()

  let key = $state('')
  let provider = $state('')
  let displayName = $state('')
  let description = $state('')
  let metaDescription = $state('')
  let primaryColor = $state(DEFAULT_MODEL_COLOR)
  let version = $state(1)
  let capabilities = $state({
    supportsImages: false,
    supportsReasoning: false,
    supportsCodeExecution: false,
    supportsFunctionCalling: true,
    maxTokens: 4096,
  })

  $effect(() => {
    if (mode === 'edit' && model) {
      key = model.key
      provider = model.provider
      displayName = model.display_name || model.name || ''
      description = model.description || ''
      metaDescription = model.meta?.description || ''
      primaryColor = typeof model.meta?.primaryColor === 'string' 
        ? model.meta.primaryColor 
        : DEFAULT_MODEL_COLOR
      version = model.version || 1
      capabilities = {
        supportsImages: model.meta?.capabilities?.supportsImages ?? false,
        supportsReasoning: model.meta?.capabilities?.supportsReasoning ?? false,
        supportsCodeExecution: model.meta?.capabilities?.supportsCodeExecution ?? false,
        supportsFunctionCalling:
          model.meta?.capabilities?.supportsFunctionCalling ?? false,
        maxTokens: model.meta?.capabilities?.maxTokens ?? 4096,
      }
    } else if (mode === 'create') {
      key = ''
      provider = ''
      displayName = ''
      description = ''
      metaDescription = ''
      primaryColor = getRandomModelColor()
      version = 1
      capabilities = {
        supportsImages: false,
        supportsReasoning: false,
        supportsCodeExecution: false,
        supportsFunctionCalling: false,
        maxTokens: 4096,
      }
    }
  })

  const title = $derived(
    mode === 'create' ? 'Create New Model' : `Edit Model: ${model?.key}`,
  )
  const submitText = $derived(mode === 'create' ? 'Create Model' : 'Update Model')
  const action = $derived(mode === 'create' ? '?/create' : '?/update')
</script>

{#if isOpen}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div
      class="m-4 max-h-screen w-full max-w-2xl overflow-y-auto rounded-lg bg-white shadow-xl"
    >
      <form
        method="POST"
        {action}
        use:enhance={() => {
          return async ({ result, update }) => {
            if (result.type === 'success') {
              onClose()
              await update()
              await invalidateAll()
            } else {
              await applyAction(result)
            }
          }
        }}
      >
        {#if mode === 'edit' && model}
          <input type="hidden" name="key" value={model.key} />
          <input type="hidden" name="version" value={version} />
        {/if}

        <input type="hidden" name="supportsImages" value={capabilities.supportsImages} />
        <input
          type="hidden"
          name="supportsReasoning"
          value={capabilities.supportsReasoning}
        />
        <input
          type="hidden"
          name="supportsCodeExecution"
          value={capabilities.supportsCodeExecution}
        />
        <input
          type="hidden"
          name="supportsFunctionCalling"
          value={capabilities.supportsFunctionCalling}
        />
        <input type="hidden" name="maxTokens" value={capabilities.maxTokens} />
        <input type="hidden" name="primaryColor" value={primaryColor} />

        <div class="p-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-bold text-base-content">{title}</h2>
            <button
              type="button"
              onclick={onClose}
              class="text-base-content/40 hover:text-base-content/60"
              aria-label="Close modal"
            >
              <X class="h-6 w-6" />
            </button>
          </div>

          <div class="space-y-4">
            {#if mode === 'edit'}
              <div>
                <label
                  for="readonly_model_key"
                  class="mb-1 block text-sm font-medium text-base-content"
                >
                  Model Key
                </label>
                <input
                  type="text"
                  id="readonly_model_key"
                  value={model?.key}
                  class="input input-bordered w-full bg-base-200"
                  readonly
                />
                <p class="mt-1 text-xs text-base-content/60">
                  Model key cannot be changed
                </p>
              </div>
            {:else}
              <div>
                <label for="key" class="mb-1 block text-sm font-medium text-base-content">
                  Model Key *
                </label>
                <input
                  type="text"
                  id="key"
                  name="key"
                  bind:value={key}
                  class="input input-bordered w-full"
                  placeholder="e.g., openai/gpt-4o"
                  required
                />
                <p class="mt-1 text-xs text-base-content/60">
                  LiteLLM format: provider/model-name
                </p>
              </div>
            {/if}

            <div>
              <label
                for="provider"
                class="mb-1 block text-sm font-medium text-base-content"
              >
                Provider *
              </label>
              <input
                type="text"
                id="provider"
                name="provider"
                bind:value={provider}
                class="input input-bordered w-full"
                placeholder="e.g., OpenAI"
                required
              />
            </div>

            <div>
              <label
                for="display_name"
                class="mb-1 block text-sm font-medium text-base-content"
              >
                Display Name *
              </label>
              <input
                type="text"
                id="display_name"
                name="display_name"
                bind:value={displayName}
                class="input input-bordered w-full"
                placeholder="e.g., GPT-4o"
                required
              />
            </div>

            <div>
              <label
                for="description"
                class="mb-1 block text-sm font-medium text-base-content"
              >
                Description
              </label>
              <textarea
                id="description"
                name="description"
                bind:value={description}
                class="textarea textarea-bordered w-full"
                placeholder="Brief description of the model"
                rows="3"
              ></textarea>
            </div>

            <div>
              <label
                for="meta_description"
                class="mb-1 block text-sm font-medium text-base-content"
              >
                Enhanced Description
              </label>
              <textarea
                id="meta_description"
                name="meta_description"
                bind:value={metaDescription}
                class="textarea textarea-bordered w-full"
                placeholder="Detailed description for model selection UI"
                rows="3"
              ></textarea>
              <p class="mt-1 text-xs text-base-content/60">
                This will be displayed in the model accordion selector
              </p>
            </div>

            <div>
              <label
                for="primary_color"
                class="mb-1 block text-sm font-medium text-base-content"
              >
                Primary Color
              </label>
              <ColorPicker
                selectedColor={primaryColor}
                onColorSelect={(color) => (primaryColor = color)}
              />
              <p class="mt-1 text-xs text-base-content/60">
                Choose a color to represent this model in the UI
              </p>
            </div>

            <CapabilitiesSection bind:capabilities disabled={false} />
          </div>
        </div>

        <div class="flex justify-end space-x-3 rounded-b-lg bg-base-200 px-6 py-4">
          <button type="button" onclick={onClose} class="btn btn-ghost">Cancel</button>
          <button type="submit" class="btn btn-primary">{submitText}</button>
        </div>
      </form>
    </div>
  </div>
{/if}
