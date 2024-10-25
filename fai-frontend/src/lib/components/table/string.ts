import { accessProperty } from '$lib/components/table/object'

const TemplateStrExtractorExp = /\{([\w.]+(\[\d+])*(\.[\w.]+(\[\d+])*)*)}/g

const fromDotPathLookUp = (match: string, dotPath: string, data: any): string =>
  accessProperty(data, dotPath, match)

export const formatTemplateStr = (
  template: string,
  values: any,
  formatFn: (
    match: string,
    variableName: string,
    values: any,
  ) => string = fromDotPathLookUp,
  replaceExp: RegExp = TemplateStrExtractorExp,
): string =>
  template.replace(replaceExp, (match, variableName: string) => {
    return formatFn(match, variableName, values)
  })
