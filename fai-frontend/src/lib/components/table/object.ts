export type PropertyAccessor<T> = (obj: T, path: string, defaultValue?: any) => any

const isObject = (input: any): input is Record<string, any> =>
  input !== null && typeof input === 'object'

const getPropertyRecursive = (obj: any, pathParts: string[], defaultValue: any): any => {
  if (pathParts.length === 0) return obj

  const [currentPart, ...remainingParts] = pathParts
  const isArrayAccess = currentPart.includes('[') && currentPart.includes(']')

  const [prop, index] = isArrayAccess
    ? currentPart.split(/\[|\]/).filter(Boolean)
    : [currentPart]
  const nextObj = isObject(obj) && obj[prop]

  return isArrayAccess && Array.isArray(nextObj)
    ? getPropertyRecursive(nextObj[Number(index)], remainingParts, defaultValue)
    : Array.isArray(obj)
      ? obj.map((item) =>
          getPropertyRecursive(item, [prop, ...remainingParts], defaultValue),
        )
      : isObject(obj)
        ? getPropertyRecursive(nextObj, remainingParts, defaultValue)
        : defaultValue
}

const getProperty: PropertyAccessor<any> = (obj, path, defaultValue = undefined) => {
  const isValidInput = (isObject(obj) || Array.isArray(obj)) && path
  const pathParts = path?.split('.') || []

  return isValidInput ? getPropertyRecursive(obj, pathParts, defaultValue) : defaultValue
}

const getPropertyFromList = (
  list: any[],
  path: string,
  defaultValue = undefined,
): any[] => list.map((item) => getProperty(item, path, defaultValue))

export const accessProperty = (
  input: any,
  path: string,
  defaultValue: any = undefined,
): any =>
  Array.isArray(input)
    ? getPropertyFromList(input, path, defaultValue)
    : getProperty(input, path, defaultValue)
