import type { ColumnFiltersColumnOptions } from 'svelte-headless-table/plugins'

export enum DisplayAs {
  auto = 'auto',
  link = 'link',
  date = 'date',
  // button = 'button',
  // markdown = 'markdown',
  // json = 'json',
}

export interface DisplayField {
  key: string
  label: string
  id?: string | null
  display?: DisplayAs
}

export enum FilterWith {
  multi_select = 'multi-select',
  search = 'search',
}

export interface DisplayColumnDef extends DisplayField {
  width?: string
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  sortOrder?: 'asc' | 'desc' | null
  filter?: FilterWith | false
  filterOptions?: [string, string][]
  filterInitialValue?: string | string[] | null
  hidden?: boolean
  hideFromSearch?: boolean
}
export type ColumnFilterMap = {
  [FilterWith.multi_select]: <Item>(
    column: DisplayColumnDef,
  ) => ColumnFiltersColumnOptions<Item, any[]>
  [FilterWith.search]: <Item>(
    column: DisplayColumnDef,
  ) => ColumnFiltersColumnOptions<Item>
}
