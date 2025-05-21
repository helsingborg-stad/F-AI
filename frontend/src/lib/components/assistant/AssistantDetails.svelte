<script lang="ts">
  import type { IAssistant, IAssistantModel } from '$lib/types.js'
  import ActionButtons from '$lib/components/Form/ActionButtons.svelte'
  import AccessSection from '$lib/components/assistant/AccessSection.svelte'
  import ToolsSection from '$lib/components/assistant/ToolsSection.svelte'
  import ModelConfigSection from '$lib/components/assistant/ModelConfigSection.svelte'
  import AvatarSection from '$lib/components/assistant/Edit/Avatar/AvatarSection.svelte'

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
    onReady = () => {
    },
  }: Props = $props()

  let formAction = $state('update')
  let assistantName = $state(assistant?.name || '')

  const collectionId = assistant?.collection?.id ? assistant.collection.id : ''

  $effect(() => {
    // Notify parent that assistant data is processed and ready, used for spinner
    if (!assistant || Object.keys(assistant).length === 0) {
      onReady()
    } else if (assistant && Object.keys(assistant).length > 0) {
      onReady()
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
</script>

{#if loading}
  <div class="flex h-screen items-center justify-center">
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>
{:else if assistant && Object.keys(assistant).length > 0}
  <div class="h-full px-1">
    <form method="POST" action="?/{formAction}" class="space-y-4 pb-8">
      <input
        type="hidden"
        name="assistant_id"
        value={assistant.id}
      />
      <input
        type="hidden"
        name="model_key"
        bind:value={selectedModelKey}
      >
      <input
        type="hidden"
        name="collection_id"
        value={collectionId}
      >

      <AvatarSection
        avatarBase64={assistant.avatar_base64}
        altImagePlaceholder={assistantName.charAt(0)}
        avatarColor=""
      />

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text">Name</span>
        </div>
        <input
          type="text"
          name="name"
          placeholder="Enter a user friendly name"
          class="input input-bordered input-sm w-full"
          required
          bind:value={assistantName}
          readonly={!canEdit}
          autocomplete="off"
          onkeydown={(e) => e.key === 'Enter' && e.preventDefault()}
        />
        <div class="label">
          <span class="label-text-alt opacity-50">{assistant.id}</span>
        </div>
      </label>

      <label class="form-control">
        <div class="label">
          <span class="label-text">Description</span>
        </div>
        <textarea
          name="description"
          class="textarea textarea-bordered h-24"
          placeholder="Provide a clear description of your assistant's purpose, capabilities, and goals. This description will be visible to users if you share this assistant."
          readonly={!canEdit}
        >{assistant.description}</textarea>
      </label>

      <label class="form-control">
        <div class="label">
          <span class="label-text">System instructions</span>
        </div>
        <textarea
          name="instructions"
          class="textarea textarea-bordered h-24"
          placeholder="You are a helpful assistant..."
          readonly={!canEdit}
        >{assistant.instructions}</textarea>
      </label>

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text">Model</span>
        </div>
        <select
          name="model"
          bind:value={selectedModelKey}
          class="select select-bordered select-sm text-sm"
          required
          disabled={!canEdit}
        >
          <option value="" disabled selected>Select a model</option>
          {#each models as model}
            <option value={model.key} selected={assistant.model === model.key}>{model.name}</option>
          {/each}
        </select>
      </label>
      <div class="space-y-2 pt-5">
        <AccessSection {canEdit} isPublic={assistant.isPublic} />
        <ToolsSection
          {canEdit}
          assistantId={assistant.id}
          collectionId={collectionId}
          collection={assistant.collection}
        />
        <ModelConfigSection {canEdit} />
      </div>
      <ActionButtons
        {canEdit}
        {canCreate}
        canDelete={true}
        onDelete={setDeleteAction}
        onCopy={setCopyAction}
        onUpdate={setUpdateAction}
      />
    </form>
  </div>
{/if}