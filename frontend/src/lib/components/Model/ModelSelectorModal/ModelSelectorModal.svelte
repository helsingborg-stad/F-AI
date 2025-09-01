<script lang="ts">
  import type { IAssistantModel } from '$lib/types.js'
  import ModalHeader from './ModalHeader.svelte'
  import ModalContent from './ModalContent.svelte'
  import ModalFooter from './ModalFooter.svelte'

  interface Props {
    models: IAssistantModel[]
    selectedKey: string | null
    canEdit: boolean
    onSelection?: (modelKey: string) => void
  }

  let {
    models = [],
    selectedKey,
    canEdit = true,
    onSelection,
  }: Props = $props()

  let dialog: HTMLDialogElement
  let tempSelectedKey = $state(selectedKey)

  $effect(() => {
    tempSelectedKey = selectedKey
  })

  export function showModal() {
    tempSelectedKey = selectedKey
    dialog.showModal()
  }

  function handleConfirm() {
    if (tempSelectedKey && onSelection) {
      onSelection(tempSelectedKey)
    }
    dialog.close()
  }

  function handleCancel() {
    tempSelectedKey = selectedKey
    dialog.close()
  }
</script>

<dialog 
  bind:this={dialog} 
  class="modal"
  oncancel={handleCancel}
>
  <div class="modal-box w-[90vw] max-w-3xl max-h-[85vh] flex flex-col 
    sm:w-[90vw] sm:max-w-3xl sm:rounded-lg 
    max-sm:w-screen max-sm:max-w-full max-sm:h-screen max-sm:max-h-full max-sm:rounded-none
    contrast-more:border-2 contrast-more:border-base-content">
    
    <ModalHeader />
    
    <ModalContent
      {models}
      bind:selectedKey={tempSelectedKey}
      {canEdit}
    />
    
    <ModalFooter
      onCancel={handleCancel}
      onConfirm={handleConfirm}
      confirmDisabled={!tempSelectedKey}
    />
  </div>

  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
