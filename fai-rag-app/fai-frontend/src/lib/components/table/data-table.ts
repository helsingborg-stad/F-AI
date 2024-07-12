import {
  Column,
  ComponentRenderConfig,
  createRender,
  createTable,
  DataColumn,
  Table,
} from 'svelte-headless-table'
import { get, readable, type Writable } from 'svelte/store'
import {
  type ColumnFilterMap,
  DisplayAs,
  type DisplayColumnDef,
  FilterWith,
} from '$lib/components/table/types'
import {
  addColumnFilters,
  addColumnOrder,
  addHiddenColumns,
  addSortBy,
  addTableFilter,
  type TablePlugin,
  type TablePluginInit,
  type TablePluginInstance,
} from 'svelte-headless-table/plugins'
import { initialSortKeys } from '$lib/components/table/sort'
import { accessProperty } from '$lib/components/table/object'
import Text from '$lib/components/Text.svelte'
import Link from '$lib/components/Link.svelte'
import { TextInput } from '$lib/components/input'
import {
  matchAnyFilter,
  searchFilter,
  textPrefixFilter,
} from '$lib/components/table/filter'
import MultiSelectFilter from '$lib/components/table/filter-controls/MultiSelectFilter.svelte'
import { normalizeToArray } from '$lib/components/table/array'
import SVG from '$lib/components/SVG.svelte'
import svelteHTML from '../../../additional-svelte-typings'

export const columnCellFactory: {
  [key in DisplayAs]: (value: any, column: DisplayColumnDef) => ComponentRenderConfig
} = {
  [DisplayAs.auto]: (value, _) =>
    createRender(Text, {
      text: value,
    }),
  [DisplayAs.date]: (value, _) =>
    createRender(Text, {
      text: new Date(value).toLocaleDateString(),
      class: 'text-xs',
    }),
  [DisplayAs.link]: (value, _) =>
    createRender(Link, {
      text: value,
      underline: true,
    }),
}

export const columnFilterFactory: ColumnFilterMap = {
  [FilterWith.multi_select]: (column) => ({
    fn: ({ value, filterValue }) =>
      !filterValue?.length ||
      filterValue.length === 0 ||
      matchAnyFilter(value, filterValue),
    render: ({ filterValue, preFilteredValues }) => {
      return createRender(MultiSelectFilter, {
        filterValue,
        preFilteredValues,
        column,
      })
    },
    initialFilterValue: normalizeToArray(column?.filterInitialValue ?? []),
  }),
  [FilterWith.search]: ({ label, filterInitialValue }) => ({
    fn: ({ value, filterValue }) =>
      !filterValue?.length ||
      filterValue.length === 0 ||
      textPrefixFilter(value, filterValue),
    initialFilterValue: filterInitialValue ?? '',
    render: ({ filterValue }) =>
      createRender(TextInput, {
        name: 'table-search',
        placeholder: 'Search',
        value: get(filterValue),
        variant: 'bordered',
        class: 'max-w-40',
        size: 'sm',
        label: label,
      }).on('input', (e) => {
        const { currentTarget } = e as EventElements
        return filterValue.set(currentTarget?.value ?? null)
      }),
  }),
}

const addColumnOptionsForColumnFilter = (column: DisplayColumnDef) =>
  column?.filter && Object.keys(columnFilterFactory).includes(column.filter)
    ? { filter: columnFilterFactory[column.filter as FilterWith](column) }
    : {}

const addColumnOptionsForSortBy = ({ sortable }: DisplayColumnDef) => ({
  sort: {
    disable: !sortable,
  },
})

const createColumn =
  <T>(table: Table<T>): ((columnDef: DisplayColumnDef) => DataColumn<T>) =>
  ({ key, label, id, sortable, display = DisplayAs.auto, ...rest }) =>
    table.column({
      accessor: (i) => accessProperty(i, key),
      id: id ?? key,
      plugins: {
        ...addColumnOptionsForSortBy({ key, label, sortable, display, ...rest }),
        ...addColumnOptionsForColumnFilter({ key, label, sortable, display, ...rest }),
      },
      header: () =>
        createRender(Text, {
          text: label,
        }),
      cell: (cell, state) =>
        columnCellFactory[display](cell.value, {
          key,
          label,
          sortable,
          display,
          ...rest,
        }),
      footer: () =>
        createRender(Text, {
          text: label,
        }),
    })

export const withIndexColumnLeft = <T>(table: Table<T>, columns: Column<T>[]) => [
  table.display({
    id: 'index',
    cell: (cell, state) => get(state.rows).indexOf(cell.row) + 1,
    header: (c) => '',
  }),
  ...columns,
]

export const withActionColumnRight = <T>(
  table: Table<T>,
  columns: Column<T>[],
  path: string = '/',
) => [
  ...columns,
  table.display({
    id: 'view_action',
    cell: (cell, state) =>
      createRender(Link, {
        class:
          'btn btn-sm btn-link -ml-1 -mr-1"  hover:btn-ghost hover:btn-accent btn-circle',
        href:
          path +
          (typeof cell?.column?.data === 'function'
            ? accessProperty(cell.column.data(cell, state), 'id', '')
            : ''),
      }).slot(
        createRender(SVG, {
          width: '20',
          src: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWV5ZSI+PHBhdGggZD0iTTIgMTJzMy03IDEwLTcgMTAgNyAxMCA3LTMgNy0xMCA3LTEwLTctMTAtN1oiLz48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIzIi8+PC9zdmc+',
        }),
      ),
    data: (cell, state) => (cell.row.isData() ? cell.row.original : {}),
    header: (c) => 'View',
  }),
]

export const useDataTable = <T>(
  dataStore: Writable<T[]>,
  columns: DisplayColumnDef[],
) => {
  const plugins = {
    sort: addSortBy<T>({
      initialSortKeys: initialSortKeys(columns),
      disableMultiSort: true,
      toggleOrder: ['desc', 'asc', undefined],
    }),
    colOrder: addColumnOrder<T>({}),
    hideColumns: addHiddenColumns<T>({
      initialHiddenColumnIds: [
        ...columns.filter(({ hidden }) => hidden).map(({ key, id }) => id ?? key),
      ],
    }),
    tableFilter: addTableFilter<T>({
      fn: ({ filterValue, value }) =>
        filterValue.trim() === '' || searchFilter(value, filterValue),
    }),
    filter: addColumnFilters<T>({}),
  }

  const table = createTable<T>(dataStore, plugins)
  const dataColumns = columns.map(createColumn(table))
  return table.createViewModel(
    withActionColumnRight(table, withIndexColumnLeft(table, dataColumns)),
  )
}
