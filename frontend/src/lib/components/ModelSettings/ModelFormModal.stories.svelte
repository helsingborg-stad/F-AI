<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ModelFormModal from './ModelFormModal.svelte'
  import { fn } from '@storybook/test'
  import { mockModels } from '$lib/mock/models.js'

  const mockModel = mockModels[0] // GPT-4o with primary color

  const { Story } = defineMeta({
    title: 'Components/ModelSettings/ModelFormModal',
    component: ModelFormModal,
    tags: ['autodocs'],
    argTypes: {
      isOpen: {
        control: 'boolean',
        description: 'Whether the modal is open',
      },
      mode: {
        control: 'radio',
        options: ['create', 'edit'],
        description: 'Modal mode - create new model or edit existing',
      },
      model: {
        control: 'object',
        description: 'Model object to edit (only used in edit mode)',
      },
      onClose: {
        action: 'onClose',
        description: 'Callback when modal is closed',
      },
    },
  })
</script>

<Story
  name="Create Mode"
  args={{
    isOpen: true,
    mode: 'create',
    onClose: fn(),
  }}
/>

<Story
  name="Edit Mode"
  args={{
    isOpen: true,
    mode: 'edit',
    model: mockModel,
    onClose: fn(),
  }}
/>
