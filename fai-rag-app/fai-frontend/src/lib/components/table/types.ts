import { type ComponentProps, type ComponentType, SvelteComponent } from 'svelte'
import { DataBodyCell, type TableState } from 'svelte-headless-table'

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
  select = 'select',
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

export interface DisplayColumnRender<T extends SvelteComponent, Item = any> {
  component: ComponentType<T>
  props: (
    value: any,
    cell: DataBodyCell<Item>,
    state: TableState<Item>,
    displayColumnDef: DisplayColumnDef,
  ) => ComponentProps<T>
}
