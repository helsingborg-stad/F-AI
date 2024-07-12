import type { ColumnFiltersColumnOptions } from 'svelte-headless-table/plugins'
import type { GoToEvent } from '$lib/types'
import type { ComponentRenderConfig } from 'svelte-headless-table'
import type { Readable } from 'svelte/store'
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

export interface DataColumnSchema extends DisplayField {
  width?: string
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  sortOrder?: 'asc' | 'desc' | null
  filter?: FilterWith | false
  filterOptions?: [string, string][]
  filterInitialValue?: string | string[] | null
  hidden?: boolean
  hideFromSearch?: boolean
  onClick?: (row: any) => void | GoToEvent
}

export type ColumnFilterMap = {
  [FilterWith.multi_select]: <Item>(
    column: DataColumnSchema,
  ) => ColumnFiltersColumnOptions<Item, any[]>
  [FilterWith.search]: <Item>(
    column: DataColumnSchema,
  ) => ColumnFiltersColumnOptions<Item>
}

export type ColumnRenderCellMap = {
  [DisplayAs.auto]: (
    value: any,
    column: DataColumnSchema,
    rowData: Readable<any>,
  ) => ComponentRenderConfig
  [DisplayAs.date]: (
    value: any,
    column: DataColumnSchema,
    rowData: Readable<any>,
  ) => ComponentRenderConfig
  [DisplayAs.link]: (
    value: any,
    column: DataColumnSchema,
    rowData: Readable<any>,
  ) => ComponentRenderConfig
}
