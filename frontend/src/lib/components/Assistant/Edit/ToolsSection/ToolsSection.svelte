<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'
  import Section from '$lib/components/Form/Section.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import type { IAssistantModel } from '$lib/types.js'

  interface Props {
    canEdit: boolean
    collectionId: string
    collections: { id: string; label: string }[]
    maxCollectionResult: string
    enableSearch: boolean
    enableReasoning: boolean
    enableImageGeneration: boolean
    enableFileUpload: boolean
    model?: IAssistantModel
  }

  let {
    canEdit,
    collectionId,
    collection,
    collections,
    enableSearch,
    enableReasoning,
    enableImageGeneration,
    model,
  }: Props = $props()

  let currentCollectionId = $state(collectionId)
  let currentFiles = $state(collection?.files || [])
  let enableSearchValue = $state(enableSearch)
  let enableReasoningValue = $state(enableReasoning)
  let enableImageGenerationValue = $state(enableImageGeneration)

  let supportsWebSearch = $derived(model?.meta?.capabilities?.supportsWebSearch ?? false)
  let supportsReasoning = $derived(model?.meta?.capabilities?.supportsReasoning ?? false)
  let supportsImageGeneration = $derived(
    model?.meta?.capabilities?.supportsImagegen ?? false,
  )
</script>

<input
  type="hidden"
  name="enable_search"
  value={supportsWebSearch ? enableSearchValue : false}
/>

<input
  type="hidden"
  name="enable_reasoning"
  value={supportsReasoning ? enableReasoningValue : false}
/>

<input
  type="hidden"
  name="enable_image_generation"
  value={supportsImageGeneration ? enableImageGenerationValue : false}
/>

<Section title={m.assistant_edit_tools_section_title()}>
  <div class="flex flex-row place-content-between items-center gap-2">
    <label for="collection_id">Documents</label>
    <select
      name="collection_id"
      id="collection_id"
      class="select select-bordered select-sm text-sm"
    >
      <option value="">(No documents)</option>
      {#each collections as collection (collection.id)}
        <option value={collection.id} selected={currentCollectionId === collection.id}
          >{collection.label}</option
        >
      {/each}
    </select>
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
