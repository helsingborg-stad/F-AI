<script lang="ts">
  import PageHeader from '$lib/components/Assistant/PageHeader.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'
  import AssistantTable from '$lib/components/Assistant/Table/AssistantTable.svelte'
  import type { IAssistant, IAssistantModel } from '$lib/types.js'
  import AssistantDetails from '$lib/components/Assistant/Edit/AssistantDetails.svelte'
  import { onMount } from 'svelte'

  interface Props {
    assistants?: IAssistant[]
    activeAssistant?: IAssistant
    models?: IAssistantModel[]
    canCreateAssistant?: boolean
    canEditActiveAssistant?: boolean
  }

  let {
    assistants = [],
    activeAssistant,
    models = [],
    canCreateAssistant = false,
    canEditActiveAssistant = false,
  }: Props = $props()

  let detailsContainer: HTMLElement
  let detailsContent: HTMLElement
  let needsScroll = $state(true)
  let isLoadingAssistant = $state(true)

  function checkOverflow() {
    if (detailsContainer && detailsContent) {
      needsScroll = detailsContent.scrollHeight > detailsContainer.clientHeight
    }
  }

  onMount(() => {
    checkOverflow()

    const resizeObserver = new ResizeObserver(() => {
      checkOverflow()
    })

    if (detailsContainer) resizeObserver.observe(detailsContainer)
    if (detailsContent) resizeObserver.observe(detailsContent)

    return () => {
      resizeObserver.disconnect()
    }
  })

  $effect(() => {
    // Wait for the DOM to update before measuring overflow
    setTimeout(checkOverflow, 0)
  })

  function handleAssistantReady() {
    isLoadingAssistant = false
  }
</script>

<div class="flex flex-col h-full">
  <PageHeader title="Assistants" {canCreateAssistant} />
  <HorizontalDivider />
  <div class="flex flex-1 w-full justify-center gap-4 overflow-hidden">
    <div class="flex-1 pl-4 overflow-hidden">
      <AssistantTable {assistants} {activeAssistant} />
    </div>
    <VerticalDivider />
    <div
      bind:this={detailsContainer}
      class={`flex-1 ${needsScroll ? 'overflow-auto' : 'overflow-hidden'} pb-4 pr-4`}
      style="max-height: calc(100vh - 120px);"
    >
      <div bind:this={detailsContent}>
        <AssistantDetails
          assistant={activeAssistant}
          canEdit={canEditActiveAssistant}
          canCreate={canCreateAssistant}
          {models}
          loading={isLoadingAssistant}
          onReady={handleAssistantReady}
        />
      </div>
    </div>
  </div>
</div>
