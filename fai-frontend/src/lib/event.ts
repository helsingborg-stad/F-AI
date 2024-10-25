import { goto } from 'elegua'
import type { GoToEventProps, EventToHandlerMap } from '$lib/types'

export const eventToHandlerMap: EventToHandlerMap = {
  GoToEvent({ url, query }: GoToEventProps): void {
    goto(url + (query ? '?' + new URLSearchParams(query).toString() : ''))
  },
}
