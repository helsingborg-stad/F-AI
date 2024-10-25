import type { GoToEvent } from '$lib/types'
import { eventToHandlerMap } from '$lib/event'
import { formatTemplateStr } from '$lib/components/table/string'

const createHandlerFromEvent = (event: GoToEvent) => (row: any) =>
  eventToHandlerMap[event.type]({
    ...event,
    url: formatTemplateStr(event.url, row),
    query: event.query,
  })

export const resolveHandler = (maybeFunction: (row: any) => void | GoToEvent) =>
  typeof maybeFunction === 'function'
    ? maybeFunction
    : createHandlerFromEvent(maybeFunction)

export const normalizeEventsToHandler =
  (maybeFunction: (row: any) => void | GoToEvent) => (row: any) =>
    resolveHandler(maybeFunction)(row)
