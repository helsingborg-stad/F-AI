<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ModelList from './ModelList.svelte'
  import { fn } from '@storybook/test'
  import { mockModels } from '$lib/mock/models.js'

  const { Story } = defineMeta({
    title: 'Components/ModelSettings/ModelList',
    component: ModelList,
    tags: ['autodocs'],
    argTypes: {
      models: {
        control: 'object',
        description: 'Array of model objects to display',
      },
      canEdit: {
        control: 'boolean',
        description: 'Whether the user can edit models',
      },
      canDelete: {
        control: 'boolean',
        description: 'Whether the user can delete models',
      },
      onEditModel: {
        action: 'onEditModel',
        description: 'Callback when edit button is clicked',
      },
      onDeleteModel: {
        action: 'onDeleteModel',
        description: 'Callback when delete button is clicked',
      },
    },
  })
</script>

<Story
  name="Default"
  args={{
    models: mockModels,
  }}
/>

<Story
  name="With Edit Permissions"
  args={{
    models: mockModels,
    canEdit: true,
    onEditModel: fn(),
  }}
/>

<Story
  name="With Full Permissions"
  args={{
    models: mockModels,
    canEdit: true,
    canDelete: true,
    onEditModel: fn(),
    onDeleteModel: fn(),
  }}
/>

<Story
  name="Empty State"
  args={{
    models: [],
    canEdit: true,
    canDelete: true,
  }}
/>

<Story
  name="Single Model"
  args={{
    models: [mockModels[0]],
    canEdit: true,
    canDelete: true,
    onEditModel: fn(),
    onDeleteModel: fn(),
  }}
/>

<Story
  name="Read Only"
  args={{
    models: mockModels,
    canEdit: false,
    canDelete: false,
  }}
/>
