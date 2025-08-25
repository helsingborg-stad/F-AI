<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Exhibit from '$lib/components/Assistant/View/Exhibit.svelte'
  import { mockExhibits } from '$lib/components/Assistant/View/storiesMockData.js'

  const { Story } = defineMeta({
    title: 'Components/Assistant/View/Exhibit',
    component: Exhibit,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={mockExhibits[0]} />
