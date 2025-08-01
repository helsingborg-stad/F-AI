<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'
  import Section from '$lib/components/Form/Section.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import FileUploadModal from '$lib/components/Assistant/Edit/FileUploadModal.svelte'
  import type { ICollection } from '$lib/types.js'
  import FilesSettings from '$lib/components/Assistant/Edit/ToolsSection/FilesSettings.svelte'

  interface Props {
    canEdit: boolean
    assistantId: string
    collectionId: string
    collection?: ICollection
    maxCollectionResult: string
    enableSearch: boolean
    enableReasoning: boolean
  }

  let {
    canEdit,
    assistantId,
    collectionId,
    collection,
    maxCollectionResult,
    enableSearch,
    enableReasoning,
  }: Props = $props()
  let fileModal: FileUploadModal
  let currentCollectionId = $state(collectionId)
  let currentFiles = $state(collection?.files || [])

  function openFilesModal() {
    if (fileModal) fileModal.showModal()
  }

  let attachingFiles = $state(false)
  let enableSearchValue = $state(enableSearch)
  let enableReasoningValue = $state(enableReasoning)
</script>

<input
  type="hidden"
  name="enable_search"
  bind:value={enableSearchValue}
>

<input
  type="hidden"
  name="enable_reasoning"
  bind:value={enableReasoningValue}
>

<Section title={m.assistant_edit_tools_section_title()}>
  <div class="flex flex-row place-content-between items-center">
    <div class="flex items-center gap-2">
      {#if collectionId}
        <button type="button" class="btn btn-xs" disabled={!canEdit}>
          <Icon icon={icons["database"]} width={16} height={16} />
        </button>
      {/if}
      {#if attachingFiles}
        <span class="loading loading-spinner loading-xs"></span>
      {/if}
      {#if !attachingFiles && collectionId}
        <span class="text-xs">Attached vector store {currentCollectionId}</span>
      {/if}
    </div>
    <div>
      <FilesSettings maxCollection={maxCollectionResult} />
      <button type="button" class="btn btn-sm" disabled={!canEdit} onclick={openFilesModal}>
        <Icon icon={icons["plus"]} width={16} height={16} />
        <span class="text-s">Files</span>
      </button>
    </div>
  </div>
  <div class="flex flex-row place-content-between items-center">
    <div class="overflow-x-auto">
      <table class="table table-xs">
        <tbody>
        {#each currentFiles as file}
          <tr>
            <td>{file.name}</td>
          </tr>
        {/each}
        </tbody>
      </table>
    </div>
  </div>
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
  <HorizontalDivider />
  <div class="flex flex-row place-content-between items-center">
    <div class="items-start">
      <InfoTooltip
        toolTip={m.assistant_edit_tools_capabilities_tooltip()}>
        <div class="text-sm font-medium select-none">{m.assistant_edit_tools_capabilities()}</div>
      </InfoTooltip>
    </div>
    <div class="form-control">
      <label class="label cursor-pointer">
        <span class="label-text me-2">{m.assistant_edit_tools_capabilities_web_search()}</span>
        <input type="checkbox" class="toggle toggle-sm" bind:checked={enableSearchValue} />
      </label>
      <label class="label cursor-pointer">
        <span class="label-text me-2">Reasoning</span>
        <input type="checkbox" class="toggle toggle-sm" bind:checked={enableReasoningValue} />
      </label>
    </div>
  </div>
  <HorizontalDivider />
</Section>

<FileUploadModal
  bind:this={fileModal} {assistantId}
  bind:uploadingFiles={attachingFiles}
  bind:collectionId={currentCollectionId}
  bind:files={currentFiles}
/>
