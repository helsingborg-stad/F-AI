<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import MainPage from '$lib/components/assistant/MainPage.svelte'
  import type { IAssistant } from '$lib/types.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/MainPage',
    component: MainPage,
    tags: ['autodocs'],
  })

  const assistants: IAssistant[] = [
    {
      id: '6808ddaffcd3461eea42133f',
      owner: 'user@example.com',
      name: 'Research Assistant',
      description: 'Helps with research tasks and information gathering',
      instructions: 'Answer questions clearly and cite sources when possible',
      model: 'gpt-4',
    },
    {
      id: '6651afc3a7b5e3c8d9f01234',
      owner: 'user@example.com',
      name: 'Code Helper',
      description: 'Provides coding assistance and debugging help',
      instructions: 'Explain code solutions with comments for clarity',
      model: 'claude-3',
    },
  ]
</script>

<Story name="Default" />

<Story name="With assistants" args={{assistants}} />