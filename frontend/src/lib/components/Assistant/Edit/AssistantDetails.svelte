<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import type { IAssistant, IAssistantModel } from '$lib/types.js'
  import ActionButtons from '$lib/components/Form/ActionButtons.svelte'
  import AccessSection from '$lib/components/Assistant/Edit/AccessSection.svelte'
  import ToolsSection from '$lib/components/Assistant/Edit/ToolsSection/ToolsSection.svelte'
  import ModelConfigSection from '$lib/components/Assistant/Edit/ModelConfigSection.svelte'
  import AvatarSection from '$lib/components/Assistant/Edit/AvatarSection.svelte'
  import ModelSelector from '$lib/components/Model/ModelSelector.svelte'

  interface Props {
    assistant?: IAssistant
    models?: IAssistantModel[]
    canCreate?: boolean
    canEdit?: boolean
    loading?: boolean
    onReady?: () => void
  }

  let {
    assistant,
    models = [],
    canCreate = false,
    canEdit = false,
    loading = false,
    onReady = () => {},
  }: Props = $props()

  let formAction = $state('update')
  let assistantName = $state(assistant?.name || '')
  let sentinelTop = $state<HTMLDivElement>()
  let sentinelBottom = $state<HTMLDivElement>()
  let buttonsWrapper = $state<HTMLDivElement>()
  let containerRef = $state<HTMLDivElement>()
  let isSticky = $state(false)
  let atBottom = $state(false)
  let containerBounds = $state({ left: 0, width: 0 })

  const collectionId = assistant?.collection?.id ? assistant.collection.id : ''

  $effect(() => {
    if (!assistant || Object.keys(assistant).length === 0) {
      onReady()
    } else if (assistant && Object.keys(assistant).length > 0) {
      onReady()
    }
  })

  $effect(() => {
    if (!sentinelTop || !sentinelBottom || !buttonsWrapper) return

    const topObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          isSticky = !entry.isIntersecting
        })
      },
      { threshold: 0 },
    )

    const bottomObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          atBottom = entry.isIntersecting
        })
      },
      { rootMargin: `0px 0px ${buttonsWrapper.offsetHeight}px 0px` },
    )

    topObserver.observe(sentinelTop)
    bottomObserver.observe(sentinelBottom)

    return () => {
      topObserver.disconnect()
      bottomObserver.disconnect()
    }
  })

  $effect(() => {
    if (!containerRef) return

    const updateBounds = () => {
      if (!containerRef) return

      const rect = containerRef.getBoundingClientRect()
      containerBounds = {
        left: rect.left,
        width: rect.width,
      }
    }

    updateBounds()
    window.addEventListener('resize', updateBounds)

    return () => {
      window.removeEventListener('resize', updateBounds)
    }
  })

  function setDeleteAction() {
    formAction = 'delete'
  }

  function setCopyAction() {
    formAction = 'copy'
  }

  function setUpdateAction() {
    formAction = 'update'
  }

  let selectedModelKey = $state(assistant ? assistant.model : '')

  let shouldStick = $derived(isSticky && !atBottom)
</script>

{#if loading}
  <div class="flex h-screen items-center justify-center">
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>
{:else if assistant && Object.keys(assistant).length > 0}
  <div class="relative h-full px-1" bind:this={containerRef}>
    <form
      method="POST"
      action="?/{formAction}"
      enctype="multipart/form-data"
      class="space-y-4 pb-8"
    >
      <input type="hidden" name="assistant_id" value={assistant.id} />
      <input type="hidden" name="collection_id" value={collectionId} />

      <AvatarSection
        avatarBase64={assistant.avatarBase64}
        altImagePlaceholder={assistantName.charAt(0)}
        primaryColor={assistant.primaryColor}
      />

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text">{m.assistant_edit_name_label()}</span>
        </div>
        <input
          type="text"
          name="name"
          placeholder={m.assistant_edit_name_placeholder()}
          class="input input-sm input-bordered w-full"
          bind:value={assistantName}
          readonly={!canEdit}
          autocomplete="off"
          onkeydown={(e) => e.key === 'Enter' && e.preventDefault()}
        />
      </label>

      <label class="form-control">
        <div class="label">
          <span class="label-text">{m.assistant_edit_description_label()}</span>
        </div>
        <textarea
          name="description"
          class="textarea textarea-bordered h-24"
          placeholder={m.assistant_edit_description_placeholder()}
          readonly={!canEdit}>{assistant.description}</textarea
        >
      </label>

      <label class="form-control">
        <div class="label">
          <span class="label-text">{m.assistant_edit_system_instruction_label()}</span>
        </div>
        <textarea
          name="instructions"
          class="textarea textarea-bordered h-24"
          placeholder={m.assistant_edit_system_instruction_placeholder()}
          readonly={!canEdit}>{assistant.instructions}</textarea
        >
      </label>

      <div class="form-control w-full">
        <div class="label">
          <span class="label-text">{m.assistant_edit_model_placeholder()}</span>
        </div>
        <ModelSelector
          {models}
          bind:selectedKey={selectedModelKey}
          {canEdit}
          name="model"
        />
      </div>

      <div class="space-y-2 pt-5">
        <AccessSection {canEdit} isPublic={assistant.isPublic} />
        <ToolsSection
          {canEdit}
          assistantId={assistant.id}
          {collectionId}
          collection={assistant.collection}
          maxCollectionResult={assistant.maxCollectionResults}
          enableSearch={assistant.enableSearch}
          enableReasoning={assistant.enableReasoning}
          enableImageGeneration={assistant.enableImageGeneration}
          enableFileUpload={assistant.enableFileUpload}
        />
        <ModelConfigSection {canEdit} />
      </div>

      <div bind:this={sentinelTop} class="h-px"></div>

      <div bind:this={buttonsWrapper} class="relative">
        <div
          class="transition-all duration-200 {shouldStick
            ? 'fixed bottom-0 z-50 mb-2 rounded-md  border-t bg-base-100 px-2 py-3'
            : ''}"
          style={shouldStick
            ? `left: ${containerBounds.left}px; width: ${containerBounds.width}px;`
            : ''}
        >
          <ActionButtons
            {canEdit}
            {canCreate}
            canDelete={true}
            onDelete={setDeleteAction}
            onCopy={setCopyAction}
            onUpdate={setUpdateAction}
          />
        </div>
        {#if shouldStick}
          <div style="height: 56px"></div>
        {/if}
      </div>
      <div bind:this={sentinelBottom} class="h-px"></div>
    </form>
  </div>
{/if}
