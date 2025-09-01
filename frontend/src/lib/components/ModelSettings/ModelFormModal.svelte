<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import { enhance, applyAction } from '$app/forms'
  import { invalidateAll } from '$app/navigation'
  
  interface Props {
    isOpen: boolean
    mode: 'create' | 'edit'
    model?: IAssistantModel | null
    onClose: () => void
  }

  let {
    isOpen = false,
    mode = 'create',
    model = null,
    onClose,
  }: Props = $props()

  let formData = $state({
    key: '',
    provider: '',
    display_name: '',
    description: '',
    meta_description: '',
    avatar_base64: '',
    version: 1,
  })

  $effect(() => {
    if (mode === 'edit' && model) {
      formData = {
        key: model.key,
        provider: model.provider,
        display_name: model.display_name || model.name || '',
        description: model.description || '',
        meta_description: model.meta?.description || '',
        avatar_base64: model.meta?.avatar_base64 || '',
        version: (model as unknown as { version?: number }).version || 1,
      }
    } else if (mode === 'create') {
      formData = {
        key: '',
        provider: '',
        display_name: '',
        description: '',
        meta_description: '',
        avatar_base64: '',
        version: 1,
      }
    }
  })

  const title = $derived(mode === 'create' ? 'Create New Model' : `Edit Model: ${model?.key}`)
  const submitText = $derived(mode === 'create' ? 'Create Model' : 'Update Model')
  const action = $derived(mode === 'create' ? '?/create' : '?/update')
</script>

{#if isOpen}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="m-4 max-h-screen w-full max-w-2xl overflow-y-auto rounded-lg bg-white shadow-xl">
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
          <input type="hidden" name="version" value={formData.version} />
        {/if}

        <div class="p-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-bold text-base-content">{title}</h2>
            <button
              type="button"
              onclick={onClose}
              class="text-base-content/40 hover:text-base-content/60"
              aria-label="Close modal"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            {#if mode === 'edit'}
              <div>
                <label for="readonly_model_key" class="mb-1 block text-sm font-medium text-base-content">
                  Model Key
                </label>
                <input
                  type="text"
                  id="readonly_model_key"
                  value={model?.key}
                  class="input input-bordered w-full bg-base-200"
                  readonly
                />
                <p class="mt-1 text-xs text-base-content/60">Model key cannot be changed</p>
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
                  bind:value={formData.key}
                  class="input input-bordered w-full"
                  placeholder="e.g., openai/gpt-4o"
                  required
                />
                <p class="mt-1 text-xs text-base-content/60">LiteLLM format: provider/model-name</p>
              </div>
            {/if}

            <div>
              <label for="provider" class="mb-1 block text-sm font-medium text-base-content">
                Provider *
              </label>
              <input
                type="text"
                id="provider"
                name="provider"
                bind:value={formData.provider}
                class="input input-bordered w-full"
                placeholder="e.g., OpenAI"
                required
              />
            </div>

            <div>
              <label for="display_name" class="mb-1 block text-sm font-medium text-base-content">
                Display Name *
              </label>
              <input
                type="text"
                id="display_name"
                name="display_name"
                bind:value={formData.display_name}
                class="input input-bordered w-full"
                placeholder="e.g., GPT-4o"
                required
              />
            </div>

            <div>
              <label for="description" class="mb-1 block text-sm font-medium text-base-content">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                bind:value={formData.description}
                class="textarea textarea-bordered w-full"
                placeholder="Brief description of the model"
                rows="3"
              ></textarea>
            </div>

            <div>
              <label for="meta_description" class="mb-1 block text-sm font-medium text-base-content">
                Enhanced Description
              </label>
              <textarea
                id="meta_description"
                name="meta_description"
                bind:value={formData.meta_description}
                class="textarea textarea-bordered w-full"
                placeholder="Detailed description for model selection UI"
                rows="3"
              ></textarea>
              <p class="mt-1 text-xs text-base-content/60">
                This will be displayed in the model accordion selector
              </p>
            </div>
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