<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ModelItem from './ModelItem.svelte'
  import { fn } from '@storybook/test'
  import { mockModels, mockModelMinimal, mockModelWithAvatar } from '$lib/mock/models.js'

  const mockModel = mockModels[0] // GPT-4o
  const mockModelDeprecated = mockModels[4] // GPT-4 Turbo (Deprecated)

  const { Story } = defineMeta({
    title: 'Components/ModelSettings/ModelItem',
    component: ModelItem,
    tags: ['autodocs'],
    argTypes: {
      model: {
        control: 'object',
        description: 'Model object to display',
      },
      canEdit: {
        control: 'boolean',
        description: 'Whether the user can edit this model',
      },
      canDelete: {
        control: 'boolean',
        description: 'Whether the user can delete this model',
      },
      onEdit: {
        action: 'onEdit',
        description: 'Callback when edit button is clicked',
      },
      onDelete: {
        action: 'onDelete',
        description: 'Callback when delete button is clicked',
      },
    },
  })
</script>

<Story
  name="Default"
  args={{
    model: mockModel,
  }}
/>

<Story
  name="With Edit Button"
  args={{
    model: mockModel,
    canEdit: true,
    onEdit: fn(),
  }}
/>

<Story
  name="With All Actions"
  args={{
    model: mockModel,
    canEdit: true,
    canDelete: true,
    onEdit: fn(),
    onDelete: fn(),
  }}
/>

<Story
  name="Minimal Model"
  args={{
    model: mockModelMinimal,
    canEdit: true,
    canDelete: true,
    onEdit: fn(),
    onDelete: fn(),
  }}
/>

<Story
  name="With Avatar"
  args={{
    model: mockModelWithAvatar,
    canEdit: true,
    canDelete: true,
    onEdit: fn(),
    onDelete: fn(),
  }}
/>

<Story
  name="Deprecated Model"
  args={{
    model: mockModelDeprecated,
    canEdit: true,
    canDelete: true,
    onEdit: fn(),
    onDelete: fn(),
  }}
/>

<Story
  name="Read Only"
  args={{
    model: mockModel,
    canEdit: false,
    canDelete: false,
  }}
/>
