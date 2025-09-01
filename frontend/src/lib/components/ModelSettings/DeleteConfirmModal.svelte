<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import { enhance, applyAction } from '$app/forms'
  import { invalidateAll } from '$app/navigation'
  import X from 'lucide-svelte/icons/x'
  import TriangleAlert from 'lucide-svelte/icons/triangle-alert'
  
  interface Props {
    isOpen: boolean
    model: IAssistantModel | null
    onClose: () => void
  }

  let {
    isOpen = false,
    model = null,
    onClose,
  }: Props = $props()

  let errorMessage = $state('')

  $effect(() => {
    if (!isOpen) {
      errorMessage = ''
    }
  })
</script>

{#if isOpen && model}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="m-4 w-full max-w-md rounded-lg bg-white shadow-xl">
      <form
        method="POST"
        action="?/delete"
        use:enhance={() => {
          return async ({ result, update }) => {
            if (result.type === 'success' && result.data?.success === true) {
              errorMessage = ''
              onClose()
              await update()
              await invalidateAll()
            } else if (result.type === 'success' && result.data?.success === false) {
              errorMessage = (() => {
                const error = result.data?.error
                if (typeof error !== 'string') return 'Failed to delete the model. Please try again.'
                if (error.includes('in use')) return 'This model cannot be deleted because it is currently being used by one or more assistants.'
                return error
              })()
            } else {
              await applyAction(result)
            }
          }
        }}
      >
        <input type="hidden" name="key" value={model.key} />

        <div class="p-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-bold text-base-content">Delete Model</h2>
            <button
              type="button"
              onclick={onClose}
              class="text-base-content/40 hover:text-base-content/60"
              aria-label="Close modal"
            >
              <X class="h-6 w-6" />
            </button>
          </div>

          {#if errorMessage}
            <div class="mb-4">
              <div class="rounded-lg border border-error bg-error/10 p-3">
                <p class="text-sm text-error-content">{errorMessage}</p>
              </div>
            </div>
          {/if}

          <div class="mb-4">
            <div class="rounded-lg border border-error/20 bg-error/10 p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <TriangleAlert class="h-8 w-8 text-error" />
                </div>
                <div class="ml-4">
                  <h3 class="text-base font-semibold text-error-content">
                    Are you sure you want to delete this model?
                  </h3>
                  <div class="mt-2 text-sm text-error-content/90">
                    <p>
                      <strong>Model:</strong>
                      {model.display_name || model.name} ({model.key})
                    </p>
                    <p><strong>Provider:</strong> {model.provider}</p>
                    <p class="mt-2">
                      This action cannot be undone. The model will be permanently deleted
                      and removed from all assistants using it.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end space-x-3 rounded-b-lg bg-base-200 px-6 py-4">
          <button type="button" onclick={onClose} class="btn btn-ghost">Cancel</button>
          <button type="submit" class="btn btn-error">Delete Model</button>
        </div>
      </form>
    </div>
  </div>
{/if}
