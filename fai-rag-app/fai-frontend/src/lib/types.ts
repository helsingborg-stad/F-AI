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
  events?: Record<string, (e: Event) => void>
}

export interface IEventDef {
  type: string
}

export interface GoToEvent extends IComponentDef {
  type: 'GoToEvent'
  url: string
  query: Record<string, any> | null
}
