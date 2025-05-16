<script module lang="ts">
  import { action } from '@storybook/addon-actions'
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import HistoryTree from '$lib/components/Menu/Chat/HistoryTree/HistoryTree.svelte'
  import dayjs from 'dayjs'
  import type { ItemOptionsType } from '$lib/types.js'

  const { Story } = defineMeta({
    title: 'Components/Menu/HistoryTree',
    component: HistoryTree,
    tags: ['autodocs'],
    argTypes: {
      historyItems: { control: 'object', description: 'List of history' },
    },
  })

  const today = dayjs().toISOString()

  function options(id: string): ItemOptionsType[] {
    return [
      { iconName: 'pencil', title: 'Rename', onClick: action(`rename ${id}`) },
      {
        iconName: 'trash',
        title: 'Delete',
        onClick: action(`delete ${id}`),
      },
    ]
  }

</script>


<Story name="Default" args={{
  highlightedIds:['a', 'd', 'e'],
  items: [
    {id: 'a', title: 'A - Lorem ipsum dolor sit amet consectetur, adipisicing elit. Impedit doloribus debitis natus, libero, pariatur, explicabo accusantium enim rerum voluptas possimus dolore illo cum praesentium sapiente facere fuga labore modi consequuntur?', options: options('A'), createdTimestamp: today },
    {id: 'b', title: 'B', options: options('B'), createdTimestamp: today },
    {id: 'c', title: 'C', options: options('C'), createdTimestamp: today },

    {id: 'd', title: 'D', options: options('D'), createdTimestamp: dayjs(today).subtract(1, 'day').toISOString() },
    {id: 'e', title: 'E', options: options('E'), createdTimestamp: dayjs(today).subtract(1, 'day').toISOString() },

    {id: 'f', title: 'F', options: options('F'), createdTimestamp: dayjs(today).subtract(2, 'day').toISOString() },
    {id: 'g', title: 'G', options: options('G'), createdTimestamp: dayjs(today).subtract(4, 'day').toISOString() },
    {id: 'h', title: 'H', options: options('H'), createdTimestamp: dayjs(today).subtract(7, 'day').toISOString() },

    {id: 'i', title: 'I', options: options('I'), createdTimestamp: dayjs(today).subtract(8, 'day').toISOString() },
    {id: 'j', title: 'J', options: options('J'), createdTimestamp: dayjs(today).subtract(15, 'day').toISOString() },
    {id: 'k', title: 'K', options: options('K'), createdTimestamp: dayjs(today).subtract(30, 'day').toISOString() },

    {id: 'l', title: 'L', options: options('L'), createdTimestamp: dayjs(today).subtract(31, 'day').toISOString() },
    {id: 'm', title: 'M', options: options('M'), createdTimestamp: dayjs(today).subtract(100, 'day').toISOString() },
  ],
  onClick: action('onClick'),
}} />
