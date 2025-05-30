<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import AssistantZoo from '$lib/components/Assistant/View/AssistantZoo.svelte'
  import { mockExhibits } from '$lib/components/Assistant/View/storiesMockData.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/View/AssistantZoo',
    component: AssistantZoo,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={{ exhibits: mockExhibits }} />