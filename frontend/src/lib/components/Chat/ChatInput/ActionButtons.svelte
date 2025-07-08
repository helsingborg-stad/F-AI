<script lang="ts">
  import AssistantPicker from '$lib/components/Menu/AssistantPicker/AssistantPicker.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import IconToggleButton from '$lib/components/Buttons/IconToggleButton.svelte'

  export interface AllowedFeature {
    id: string
    title: string
    icon: string
  }

  interface Props {
    allowedFeatures: AllowedFeature[]
    enabledFeatureIds: string[]
    assistants: IAssistantMenu[],
    selectedAssistantId: string,
    disableAssistantPicker: boolean
  }

  let {
    allowedFeatures,
    enabledFeatureIds = $bindable(),
    assistants,
    selectedAssistantId = $bindable(),
    disableAssistantPicker,
  }: Props = $props()

  const isFeatureEnabled = (featureId: string) => enabledFeatureIds.includes(featureId)
  const setFeatureEnabled = (featureId: string, enabled: boolean) => {
    enabledFeatureIds = enabled ? [...enabledFeatureIds, featureId] : enabledFeatureIds.filter(id => id !== featureId)
  }

  $effect(() => {
    const filteredEnabledFeatures = enabledFeatureIds.filter(id => allowedFeatures.map(f => f.id).includes(id))
    const isDifferent = enabledFeatureIds.some((id, i) => id !== filteredEnabledFeatures[i])
    if (isDifferent) {
      enabledFeatureIds = filteredEnabledFeatures
    }
  })
</script>

<div class="flex flex-row pr-3 gap-1">
  {#each allowedFeatures as feature}
    <IconToggleButton
      title={feature.title}
      icon={feature.icon}
      bind:value={
        () => isFeatureEnabled(feature.id),
        (v) => setFeatureEnabled(feature.id, v)
      }
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
