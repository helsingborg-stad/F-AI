<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import PageHeader from './PageHeader.svelte'
  import { fn } from '@storybook/test'

  const { Story } = defineMeta({
    title: 'Components/ModelSettings/PageHeader',
    component: PageHeader,
    tags: ['autodocs'],
    argTypes: {
      title: {
        control: 'text',
        description: 'Page title',
      },
      description: {
        control: 'text',
        description: 'Page description',
      },
      canCreate: {
        control: 'boolean',
        description: 'Whether the user can create models',
      },
      onCreateClick: {
        action: 'onCreateClick',
        description: 'Callback when create button is clicked',
      },
    },
  })
</script>

<Story name="Default" />

<Story
  name="With Create Button"
  args={{
    canCreate: true,
    onCreateClick: fn(),
  }}
/>

<Story
  name="Custom Title and Description"
  args={{
    title: 'AI Model Configuration',
    description: 'Configure and manage the AI models used throughout the system.',
    canCreate: true,
    onCreateClick: fn(),
  }}
/>

<Story
  name="Read Only"
  args={{
    title: 'Available Models',
    description: 'View the AI models available in the system.',
    canCreate: false,
  }}
/>
