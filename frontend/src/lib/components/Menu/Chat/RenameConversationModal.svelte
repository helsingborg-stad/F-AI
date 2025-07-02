<script lang="ts">
  interface Props {
    onSave: (conversationId: string, title: string) => void
  }

  let { onSave }: Props = $props()

  let title: string = $state('')
  let conversationId: string = $state('')

  let dialog: HTMLDialogElement

  export function showModal(id: string, currentTitle: string) {
    conversationId = id
    title = currentTitle

    dialog.showModal()
  }

  function handleSave(conversationId: string, title: string) {
    onSave(conversationId, title)
    dialog.close()
  }
</script>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box">
    <h3 class="text-lg font-bold">Rename chat</h3>
    <div class="gap-2">
      <input
        type="text"
        bind:value={title}
        class="input input-bordered w-full mt-3 px-3 py-2"
        onkeydown={e => e.key === 'Enter' && handleSave(conversationId, title)}
      />
      <div class="flex flex-row-reverse gap-2 mt-4">
        <button class="btn btn-outline min-w-24" onclick={() => handleSave(conversationId, title)}>Save</button>
        <button class="btn min-w-24" onclick={() => dialog.close()}>Cancel</button>
      </div>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
