<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import ModelAvatar from './ModelAvatar.svelte'
  import codingAssistantAvatar from '$stories/assets/avatar/coding-assistant.png'

  const { Story } = defineMeta({
    title: 'Components/Model/ModelAvatar',
    component: ModelAvatar,
    tags: ['autodocs'],
    parameters: {
      layout: 'centered',
    },
    argTypes: {
      avatar: {
        control: 'text',
        description: 'Base64 encoded avatar image or URL',
      },
      provider: {
        control: 'text',
        description: 'Provider name used for initials when no avatar is provided',
      },
      primaryColor: {
        control: 'color',
        description: 'Background color for the initials avatar',
      },
      isSelected: {
        control: 'boolean',
        description: 'Whether the model is currently selected',
      },
      size: {
        control: { type: 'select', options: ['sm', 'md'] },
        description: 'Size of the avatar',
      },
    },
  })

  const sampleAvatar = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiMxMEEzN0YiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAxOGMtNC40MSAwLTgtMy41OS04LThzMy41OS04IDgtOCA4IDMuNTkgOCA4LTMuNTkgOC04IDh6bTAtMTJjLTIuMjEgMC00IDEuNzktNCA0czEuNzkgNCA0IDQgNC0xLjc5IDQtNC0xLjc5LTQtNC00eiIvPjwvc3ZnPg=='
</script>

<Story name="Default" args={{
  provider: 'OpenAI',
  primaryColor: '#10A37F',
  isSelected: false,
}} />

<Story name="With Avatar Image" args={{
  avatar: sampleAvatar,
  provider: 'OpenAI',
  primaryColor: '#10A37F',
  isSelected: false,
}} />

<Story name="Selected State" args={{
  provider: 'Anthropic',
  primaryColor: '#D97757',
  isSelected: true,
}} />

<Story name="Small Size" args={{
  provider: 'Mistral',
  primaryColor: '#FF6B35',
  isSelected: false,
  size: 'sm',
}} />

<Story name="Medium Size" args={{
  provider: 'Google',
  primaryColor: '#4285F4',
  isSelected: false,
  size: 'md',
}} />

<Story name="With PNG Avatar" args={{
  avatar: codingAssistantAvatar,
  provider: 'AI Assistant',
  primaryColor: '#10A37F',
  isSelected: false,
}} />
