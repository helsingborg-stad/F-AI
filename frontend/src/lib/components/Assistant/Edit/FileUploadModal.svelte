<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { enhance } from '$app/forms'
  import type { SubmitFunction } from '@sveltejs/kit'
  import type { ICollectionFiles } from '$lib/types.js'

  interface Props {
    assistantId: string
    uploadingFiles?: boolean
    collectionId: string
    files: ICollectionFiles[]
  }

  let {
    assistantId,
    uploadingFiles = $bindable(false),
    collectionId = $bindable(),
    files = $bindable(),
  }: Props = $props()
  let dialog: HTMLDialogElement

  export function showModal() {
    dialog.showModal()
  }

  function handleEnhance(): ReturnType<SubmitFunction> {
    uploadingFiles = true
    files = []

    return async ({ update, result }) => {
      if (result.data && result.type === 'success') {
        collectionId = result.data.collection.id
        files = result.data.collection.files
        dialog.close()
      }

      await update()
      uploadingFiles = false
    }
  }
</script>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box">
    <h3 class="text-lg font-bold">{m.assistant_edit_tools_file_attach()}</h3>
    <p class="py-4">{m.assistant_edit_tools_file_attach_user_info()}</p>
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
          type="hidden"
          name="label"
          value="collection"
        >
        <input
          type="hidden"
          name="embedding_model"
          value="default"
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
              <span class="text-s">{m.assistant_edit_tools_file_attach()}</span>
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
