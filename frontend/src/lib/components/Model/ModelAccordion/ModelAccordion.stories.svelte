<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ModelAccordion from './ModelAccordion.svelte'
  import type { IAssistantModel } from '$lib/types.js'

  const mockModels: IAssistantModel[] = [
    {
      key: 'openai/gpt-4o',
      provider: 'OpenAI',
      display_name: 'GPT-4o',
      name: 'GPT-4o',
      meta: {
        description:
          'Advanced multimodal model that can process text, images, and audio with superior reasoning capabilities.',
      },
    },
    {
      key: 'openai/gpt-3.5-turbo',
      provider: 'OpenAI',
      display_name: 'GPT-3.5 Turbo',
      name: 'GPT-3.5 Turbo',
      meta: {
        description:
          'Fast and cost-effective model ideal for most conversational AI and text generation tasks.',
      },
    },
    {
      key: 'anthropic/claude-3-7-sonnet-latest',
      provider: 'Anthropic',
      display_name: 'Claude 3.7 Sonnet',
      name: 'Claude 3.7 Sonnet',
      meta: {
        description:
          "Anthropic's most capable model with excellent reasoning, coding, and analysis capabilities.",
      },
    },
    {
      key: 'mistral/mistral-large-latest',
      provider: 'Mistral',
      display_name: 'Mistral Large',
      name: 'Mistral Large',
      meta: {
        description:
          "Mistral's flagship model with strong performance across diverse language tasks.",
      },
    },
  ]

  const mockModelsWithCustomAvatars: IAssistantModel[] = [
    {
      key: 'openai/gpt-4o',
      provider: 'OpenAI',
      display_name: 'GPT-4o',
      name: 'GPT-4o',
      meta: {
        description: 'Advanced multimodal model with custom avatar',
        avatar_base64:
          'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiMxMEEzN0YiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAxOGMtNC40MSAwLTgtMy41OS04LThzMy41OS04IDgtOCA4IDMuNTkgOCA4LTMuNTkgOC04IDh6bTAtMTJjLTIuMjEgMC00IDEuNzktNCA0czEuNzkgNCA0IDQgNC0xLjc5IDQtNC0xLjc5LTQtNC00eiIvPjwvc3ZnPg==',
      },
    },
  ]

  const { Story } = defineMeta({
    title: 'Components/Model/ModelAccordion',
    component: ModelAccordion,
    tags: ['autodocs'],
    argTypes: {
      models: {
        control: 'object',
        description: 'Array of model objects to display',
      },
      selectedKey: {
        control: 'text',
        description: 'Currently selected model key',
      },
      canEdit: {
        control: 'boolean',
        description: 'Whether the user can select models',
      },
      name: {
        control: 'text',
        description: 'Form field name for the hidden input',
      },
    },
  })
</script>

<Story
  name="Default"
  args={{
    models: mockModels,
    selectedKey: 'openai/gpt-4o',
    canEdit: true,
    name: 'model',
  }}
/>

<Story
  name="Disabled State"
  args={{
    models: mockModels,
    selectedKey: null,
    canEdit: false,
    name: 'model',
  }}
/>

<Story
  name="Pre-selected"
  args={{
    models: mockModels,
    selectedKey: 'anthropic/claude-3-7-sonnet-latest',
    canEdit: true,
    name: 'model',
  }}
/>

<Story
  name="With Custom Avatar"
  args={{
    models: mockModelsWithCustomAvatars,
    selectedKey: 'openai/gpt-4o',
    canEdit: true,
    name: 'model',
  }}
/>

<Story
  name="Empty State"
  args={{
    models: [],
    selectedKey: null,
    canEdit: true,
    name: 'model',
  }}
/>

<Story
  name="Single Model"
  args={{
    models: [mockModels[0]],
    selectedKey: mockModels[0].key,
    canEdit: true,
    name: 'model',
  }}
/>
