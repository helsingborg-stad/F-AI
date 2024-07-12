import type { SvelteComponent } from 'svelte'

type addPrefixToObject<T, P extends string> = {
  [K in keyof T as K extends string ? `${P}${K}` : never]: T[K]
}

/**
 * IComponentDef interface represents a base component definition (fetched from server as json).
 * @interface
 * @property {string} type - The type of the component.
 * @property {IComponentDef[]} [components] - The optional array of child component definitions.
 */
export interface IComponentDef {
  type: string
  components?: IComponentDef[]
  slot?: IComponentDef[] | IComponentDef

  [key: string]:
    | any
    | addPrefixToObject<IComponentDef[] | IComponentDef, 'slot.'>
    | addPrefixToObject<IComponentDef[] | IComponentDef, 'on:'>
}

/**
 * IRenderableComponent interface represents a renderable component built from a component definition.
 * @interface
 * @property {typeof SvelteComponent} type - The type of the component which should be a SvelteComponent.
 * @property {any} props - The properties of the component.
 */
export interface IRenderableComponent {
  component: typeof SvelteComponent
  type: typeof SvelteComponent
  props: any
  components?: IRenderableComponent[]

  slots?: Record<string, IRenderableComponent[]>
  events?: Record<string, (e: AnyEvent) => void>
}

export enum EventType {
  GoTo = 'GoToEvent',
}

export interface IEventDef {
  type: EventType
}

export interface GoToEventProps {
  url: string
  query: Record<string, any> | null
}

export interface GoToEvent extends IEventDef, GoToEventProps {
  type: EventType.GoTo
}

export interface EventToHandlerMap {
  [EventType.GoTo]: ({ url, query }: GoToEventProps) => void
}

export type AnyEvent = GoToEvent
