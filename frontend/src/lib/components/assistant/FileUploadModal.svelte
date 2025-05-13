<script lang="ts">
  import { enhance } from '$app/forms'
  import type { SubmitFunction } from '@sveltejs/kit'

  interface Props {
    assistantId: string;
    uploadingFiles?: boolean
  }

  let { assistantId, uploadingFiles = $bindable(false) }: Props = $props()
  let dialog: HTMLDialogElement

  export function showModal() {
    dialog.showModal()
  }

  function handleEnhance(): ReturnType<SubmitFunction> {
    uploadingFiles = true

    return async ({ update, result }) => {
      if (result.type === 'redirect') {
        window.location.href = result.location
        return
      }

      await update()
      uploadingFiles = false
    }
  }
</script>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box">
    <h3 class="text-lg font-bold">Attach Files</h3>
    <p class="py-4">Select one or more files to attach to your assistant.</p>
    <form
      method="POST"
      action="?/uploadFiles"
      enctype="multipart/form-data"
      use:enhance={handleEnhance}
    >
      <div class="space-y-2">
        <input
          type="hidden"
          name="assistant_id"
          value={assistantId}
        >
        <input
          name="files"
          type="file"
          class="file-input file-input-sm w-full max-w-xs"
          multiple
          required
          disabled={uploadingFiles}
        />
        <div>
          <button
            type="submit"
            class="btn btn-sm
            btn-success
            text-white"
            disabled={uploadingFiles}
          >
            {#if uploadingFiles}
              <span class="loading loading-spinner loading-xs"></span>
            {:else}
              <span class="text-s">Attach</span>
            {/if}
          </button>
        </div>
      </div>
    </form>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>