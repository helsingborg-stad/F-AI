<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import type { IAssistantModel } from '$lib/types.js'
  import PageHeader from '$lib/components/ModelSettings/PageHeader.svelte'
  import ModelList from '$lib/components/ModelSettings/ModelList.svelte'
  import ModelFormModal from '$lib/components/ModelSettings/ModelFormModal.svelte'
  import DeleteConfirmModal from '$lib/components/ModelSettings/DeleteConfirmModal.svelte'

  let { data } = $props()
  
  const models = $derived(data.models || [])
  const modelPermissions = $derived(data.modelPermissions || {
    canRead: false,
    canWrite: false,
    canDelete: false,
    isAdmin: false,
  })

  let showCreateModal = $state(false)
  let showEditModal = $state(false)
  let showDeleteModal = $state(false)
  let editingModel: IAssistantModel | null = $state(null)
  let deletingModel: IAssistantModel | null = $state(null)

  function openCreateModal() {
    showCreateModal = true
  }

  function openEditModal(model: IAssistantModel) {
    editingModel = model
    showEditModal = true
  }

  function openDeleteModal(model: IAssistantModel) {
    deletingModel = model
    showDeleteModal = true
  }

  function closeCreateModal() {
    showCreateModal = false
  }

  function closeEditModal() {
    showEditModal = false
    editingModel = null
  }

  function closeDeleteModal() {
    showDeleteModal = false
    deletingModel = null
  }
</script>

<div class="mx-auto max-w-4xl p-6">
  <PageHeader 
    canCreate={modelPermissions.canWrite}
    onCreateClick={openCreateModal}
  />

  <ModelList
    {models}
    canEdit={modelPermissions.canWrite}
    canDelete={modelPermissions.canDelete}
    onEditModel={openEditModal}
    onDeleteModel={openDeleteModal}
  />
</div>

<ModelFormModal
  isOpen={showCreateModal}
  mode="create"
  onClose={closeCreateModal}
/>

<ModelFormModal 
  isOpen={showEditModal}
  mode="edit"
  model={editingModel}
  onClose={closeEditModal}
/>

<DeleteConfirmModal
  isOpen={showDeleteModal}
  model={deletingModel}
  onClose={closeDeleteModal}
/>
