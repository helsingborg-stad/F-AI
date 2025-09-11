<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import IconToggleButton from '$lib/components/Buttons/IconToggleButton.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import IconButton from '$lib/components/Buttons/IconButton.svelte'

  export interface AllowedFeature {
    id: string
    title: string
    icon: string
  }

  interface Props {
    allowedFeatures: AllowedFeature[]
    enabledFeatureIds: string[]
    assistants: IAssistantMenu[]
    selectedAssistantId: string
    disableAssistantPicker: boolean
    onFilesChanged: (files: File[]) => void
    canChangeFiles: boolean
  }

  let {
    allowedFeatures,
    enabledFeatureIds = $bindable(),
    assistants,
    selectedAssistantId = $bindable(),
    disableAssistantPicker,
    onFilesChanged,
    canChangeFiles,
  }: Props = $props()

  const isFeatureEnabled = (featureId: string) => enabledFeatureIds.includes(featureId)
  const setFeatureEnabled = (featureId: string, enabled: boolean) => {
    enabledFeatureIds = enabled
      ? [...enabledFeatureIds, featureId]
      : enabledFeatureIds.filter((id) => id !== featureId)
  }

  $effect(() => {
    const filteredEnabledFeatures = enabledFeatureIds.filter((id) =>
      allowedFeatures.map((f) => f.id).includes(id),
    )
    const isDifferent = enabledFeatureIds.some(
      (id, i) => id !== filteredEnabledFeatures[i],
    )
    if (isDifferent) {
      enabledFeatureIds = filteredEnabledFeatures
    }
  })

  let inlineFileInput: HTMLInputElement

  function showInlineFileDialog() {
    inlineFileInput.click()
  }

  function onInlineFilesChanged(ev: Event) {
    const element = ev.currentTarget as HTMLInputElement
    const files: File[] = element.files ? Array.from(element.files) : []
    onFilesChanged(files)
  }
</script>

<div class="flex flex-row items-center gap-1 pr-3">
  <div class="hidden">
    <input
      bind:this={inlineFileInput}
      type="file"
      multiple
      disabled={!canChangeFiles}
      onchange={onInlineFilesChanged}
    />
  </div>
  <IconButton
    icon={icons.filePlus}
    tooltip={'Add Files'}
    onClick={showInlineFileDialog}
    disabled={!canChangeFiles}
  />
  {#each allowedFeatures as feature}
    <IconToggleButton
      title={feature.title}
      icon={feature.icon}
      bind:value={() => isFeatureEnabled(feature.id),
      (v) => setFeatureEnabled(feature.id, v)}
    />
  {/each}
  <div class="ml-auto">
    <AssistantPicker
      {assistants}
      disabled={disableAssistantPicker}
      bind:selectedAssistantId
    />
  </div>
</div>
