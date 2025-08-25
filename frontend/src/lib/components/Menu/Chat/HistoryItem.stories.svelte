<script module lang="ts">
  import { fn } from '@storybook/test'
  import { action } from '@storybook/addon-actions'
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import HistoryItem from '$lib/components/Menu/Chat/HistoryItem.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/HistoryItem',
    component: HistoryItem,
    tags: ['autodocs'],
    argTypes: {
      title: { control: 'text' },
    },
  })
</script>

<Story
  name="Default"
  args={{
    title: 'Hello World',
    options: [],
    onClick: fn(),
  }}
/>

<Story
  name="With Options"
  args={{
    title: 'Hello World',
    options: [
      { iconName: 'copy', title: 'Copy', onClick: action('copy option') },
      { iconName: 'trash', title: 'Delete', onClick: action('delete option') },
    ],
    onClick: action('click'),
  }}
/>

<Story
  name="With Long Title"
  args={{
    title:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Commodi, consequatur debitis dicta!',
    options: [
      { iconName: 'copy', title: 'Copy', onClick: action('copy option') },
      { iconName: 'trash', title: 'Delete', onClick: action('delete option') },
    ],
    onClick: action('click'),
  }}
/>
