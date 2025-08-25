<script module>
  import { fn } from '@storybook/test'
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import HistoryItemOptions from '$lib/components/Menu/Chat/HistoryItemOptions.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/HistoryItemOptions',
    component: HistoryItemOptions,
    tags: ['autodocs'],
    argTypes: {
      iconName: {
        control: 'text',
      },
      title: { control: 'text' },
    },
  })
</script>

<Story name="Default" args={{ iconName: 'trash', title: 'Delete', onClick: fn() }} />
