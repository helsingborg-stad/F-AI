<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'
  import Section from '$lib/components/Form/Section.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import FileUploadModal from '$lib/components/Assistant/Edit/FileUploadModal.svelte'
  import type { ICollection, IAssistantModel } from '$lib/types.js'
  import FilesSettings from '$lib/components/Assistant/Edit/ToolsSection/FilesSettings.svelte'

  interface Props {
    canEdit: boolean
    assistantId: string
    collectionId: string
    collection?: ICollection
    maxCollectionResult: string
    enableSearch: boolean
    enableReasoning: boolean
    enableImageGeneration: boolean
    enableFileUpload: boolean
    model?: IAssistantModel
  }

  let {
    canEdit,
    assistantId,
    collectionId,
    collection,
    maxCollectionResult,
    enableSearch,
    enableReasoning,
    enableImageGeneration,
    enableFileUpload,
    model
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
  let enableImageGenerationValue = $state(enableImageGeneration)

  let supportsWebSearch = $derived(model?.meta?.capabilities?.supportsWebSearch ?? false)
  let supportsReasoning = $derived(model?.meta?.capabilities?.supportsReasoning ?? false)
  let supportsImageGeneration = $derived(model?.meta?.capabilities?.supportsImagegen ?? false)
</script>

<input type="hidden" name="enable_search" value={supportsWebSearch ? enableSearchValue : false} />

<input type="hidden" name="enable_reasoning" value={supportsReasoning ? enableReasoningValue : false} />

<input
  type="hidden"
  name="enable_image_generation"
  value={supportsImageGeneration ? enableImageGenerationValue : false}
/>

<Section title={m.assistant_edit_tools_section_title()}>
  <div class="flex flex-row place-content-between items-center">
    <div class="flex items-center gap-2">
      {#if collectionId}
        <button type="button" class="btn btn-xs" disabled={!canEdit || !enableFileUpload}>
          <Icon icon={icons['database']} width={16} height={16} />
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
      <button
        type="button"
        class="btn btn-sm"
        disabled={!canEdit || !enableFileUpload}
        onclick={openFilesModal}
      >
        <Icon icon={icons['plus']} width={16} height={16} />
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
        toolTip="Function calling lets you describe custom functions of your app or external APIs to the assistant."
      >
        <div class="select-none text-sm font-medium">Functions</div>
      </InfoTooltip>
    </div>
    <div>
      <button type="button" class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons['plus']} width={16} height={16} />
        <span class="text-s">Functions</span>
      </button>
    </div>
  </div>
  <HorizontalDivider />
  <div class="flex flex-row place-content-between items-center">
    <div class="items-start">
      <InfoTooltip toolTip={m.assistant_edit_tools_capabilities_tooltip()}>
        <div class="select-none text-sm font-medium">
          {m.assistant_edit_tools_capabilities()}
        </div>
      </InfoTooltip>
    </div>
    <div class="form-control">
      {#if supportsWebSearch}
        <label class="label cursor-pointer">
          <span class="label-text me-2"
            >{m.assistant_edit_tools_capabilities_web_search()}</span
          >
          <input
            type="checkbox"
            class="toggle toggle-sm"
            bind:checked={enableSearchValue}
            disabled={!canEdit}
          />
        </label>
      {:else}
        <label class="label cursor-not-allowed opacity-50">
          <span class="label-text me-2"
            >{m.assistant_edit_tools_capabilities_web_search()}</span
          >
          <input
            type="checkbox"
            class="toggle toggle-sm"
            checked={false}
            disabled={true}
          />
        </label>
      {/if}

      {#if supportsReasoning}
        <label class="label cursor-pointer">
          <span class="label-text me-2">Reasoning</span>
          <input
            type="checkbox"
            class="toggle toggle-sm"
            bind:checked={enableReasoningValue}
            disabled={!canEdit}
          />
        </label>
      {:else}
        <label class="label cursor-not-allowed opacity-50">
          <span class="label-text me-2">Reasoning</span>
          <input
            type="checkbox"
            class="toggle toggle-sm"
            checked={false}
            disabled={true}
          />
        </label>
      {/if}

      {#if supportsImageGeneration}
        <label class="label cursor-pointer">
          <span class="label-text me-2">Image Generation</span>
          <input
            type="checkbox"
            class="toggle toggle-sm"
            bind:checked={enableImageGenerationValue}
            disabled={!canEdit}
          />
        </label>
      {:else}
        <label class="label cursor-not-allowed opacity-50">
          <span class="label-text me-2">Image Generation</span>
          <input
            type="checkbox"
            class="toggle toggle-sm"
            checked={false}
            disabled={true}
          />
        </label>
      {/if}
    </div>
  </div>
  <HorizontalDivider />
</Section>

<FileUploadModal
  bind:this={fileModal}
  {assistantId}
  bind:uploadingFiles={attachingFiles}
  bind:collectionId={currentCollectionId}
  bind:files={currentFiles}
/>
