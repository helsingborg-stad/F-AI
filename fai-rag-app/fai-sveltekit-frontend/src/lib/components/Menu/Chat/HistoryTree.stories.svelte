<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/Chat/History',
    component: HistoryTree,
    tags: ['autodocs'],
    argTypes: {
      historyItems: { control: 'object', description: 'List of history' },
    },
  })

  const renameOption = {
    iconName: 'pencil',
    title: 'Rename',
    onClick: () => {},
  }

  const removeOption = {
    iconName: 'trash',
    title: 'Remove',
    onClick: () => {},
  }

  const today = new Date()
  const todaysItems = {
    title: 'Some conversation',
    itemOptions: [renameOption, removeOption],
    created: today,
  }

  const yesterdayItems = {
    title: 'Some conversation',
    itemOptions: [renameOption, removeOption],
    created: new Date(today.getTime() - 24 * 60 * 60 * 1000),
  }

  const previousSevenDaysItems = {
    title: 'Some conversation',
    itemOptions: [renameOption, removeOption],
    created: new Date(today.getTime() - 2 * 24 * 60 * 60 * 1000),
  }

  const lastMonthItems = {
    title: 'Some conversation',
    itemOptions: [renameOption, removeOption],
    created: new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000),
  }

  const olderItems = {
    title: 'Some conversation',
    itemOptions: [renameOption, removeOption],
    created: new Date(today.getTime() - 60 * 24 * 60 * 60 * 1000),
  }

  const sampleArgs = {
    historyItems: [
      todaysItems,
      todaysItems,
      todaysItems,
      yesterdayItems,
      yesterdayItems,
      previousSevenDaysItems,
      lastMonthItems,
      lastMonthItems,
      olderItems,
      olderItems,
      olderItems,
      olderItems,
      olderItems,
    ],
  }
</script>

<Story name="Tree" args={sampleArgs} />
