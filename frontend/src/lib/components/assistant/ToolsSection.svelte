<script lang="ts">
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'
  import Section from '$lib/components/Form/Section.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import FileUploadModal from '$lib/components/assistant/FileUploadModal.svelte'

  const FILE_MODAL_ID = 'files_modal'

  interface Props {
    canEdit: boolean
    assistantId: string
    collectionId: string
  }

  let { canEdit, assistantId, collectionId }: Props = $props()

  function openFilesModal() {
    const modal = document.getElementById(FILE_MODAL_ID) as HTMLDialogElement
    if (modal) modal.showModal()
  }

  let attachingFiles = $state(false)
</script>

<Section title={"Tools"}>
  <div class="flex flex-row place-content-between items-center">
    <div class="flex flex-row gap-2">
      <input type="checkbox" class="toggle toggle-sm toggle-success" disabled={!canEdit} />
      <InfoTooltip
        toolTip="File Search enables the assistant with knowledge from files that you or your users upload.">
        <div class="text-sm font-medium select-none">File search</div>
      </InfoTooltip>
    </div>
    <div>
      <button type="button" class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons["settings"]} width={16} height={16} />
      </button>
      <button type="button" class="btn btn-sm" disabled={!canEdit} onclick={openFilesModal}>
        <Icon icon={icons["plus"]} width={16} height={16} />
        <span class="text-s">Files</span>
      </button>
    </div>
  </div>

  {#if collectionId || attachingFiles}
    <div class="flex flex-row place-content-between items-center">
      <div class="flex items-center gap-2">
        <button type="button" class="btn btn-xs" disabled={!canEdit}>
          <Icon icon={icons["database"]} width={16} height={16} />
        </button>
        {#if attachingFiles}
          <span class="loading loading-spinner loading-xs"></span>
        {:else }
          <span class="text-xs">Attached vector store {collectionId}</span>
        {/if}
      </div>
    </div>
  {/if}

  <HorizontalDivider />
  <div class="flex flex-row place-content-between items-center">
    <div>
      <InfoTooltip
        toolTip="Function calling lets you describe custom functions of your app or external APIs to the assistant.">
        <div class="text-sm font-medium select-none">Functions</div>
      </InfoTooltip>
    </div>
    <div>
      <button type="button" class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons["plus"]} width={16} height={16} />
        <span class="text-s">Functions</span>
      </button>
    </div>
  </div>
</Section>

<FileUploadModal dialogId={FILE_MODAL_ID} {assistantId} bind:uploadingFiles={attachingFiles} />
