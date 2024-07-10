export const countResults = <T>(rows: any[], preFiltered: any[]): [number, number] => {
    return rows.length === preFiltered.length ? [rows.length, rows.length] : [rows.length, preFiltered.length]
}
export const normalizeToArray = (v: string | string[] | null) => Array.isArray(v) ? v : v ? [v] : []


export const getDistinct = (items: any[]) => Array.from(new Set(items))


export const normalizeFlatten = (items: any[]) => items.flat(Infinity)

export const countMatches = (value: string | string[], filterValue: string) =>
    normalizeToArray(value).filter(v => String(v).toLowerCase().includes(String(filterValue).toLowerCase().trim())).length