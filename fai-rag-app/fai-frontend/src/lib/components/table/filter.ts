import { normalizeToArray } from '$lib/components/table/array'

export const matchInFilter = (value: string | string[], filterValue: string) =>
  normalizeToArray(value).includes(filterValue)
export const matchAnyFilter = (value: string | string[], filterValue: string[]) =>
  filterValue.some((fv) => normalizeToArray(value).includes(fv))
export const matchAllFilter = (value: string | string[], filterValue: string[]) =>
  filterValue.every((fv) => normalizeToArray(value).includes(fv))

export const textPrefixFilter = (value: string | string[], filterValue: string) =>
  normalizeToArray(value).some((v) =>
    String(v).toLowerCase().startsWith(String(filterValue).toLowerCase().trim()),
  )

export const searchFilter = (value: string | string[], filterValue: string) =>
  normalizeToArray(value).some((v) =>
    String(v).toLowerCase().includes(String(filterValue).toLowerCase().trim()),
  )
