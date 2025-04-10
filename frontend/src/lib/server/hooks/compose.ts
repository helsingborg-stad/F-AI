import type { RequestEvent } from '@sveltejs/kit'

type RequestEventType = RequestEvent<Partial<Record<string, string>>, string | null>
type RequestEventHandler = (event: RequestEventType) => Promise<RequestEventType>

/**
 * Composes multiple async event handlers into a single function
 * @param {...RequestEventHandler[]} fns - Event handler functions to compose
 * @returns {RequestEventHandler} - Composed event handler function
 */
export function compose(...fns: RequestEventHandler[]): RequestEventHandler {
  return async (initialEvent: RequestEventType): Promise<RequestEventType> => {
    return fns.reduce(
      async (eventPromise, fn) => {
        const event = await eventPromise
        return fn(event)
      },
      Promise.resolve(initialEvent)
    )
  }
}