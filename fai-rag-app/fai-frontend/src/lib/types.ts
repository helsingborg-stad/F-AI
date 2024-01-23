import type {SvelteComponent} from "svelte";

/**
 * IComponentDef interface represents a base component definition (fetched from server as json).
 * @interface
 * @property {string} type - The type of the component.
 * @property {IComponentDef[]} [components] - The optional array of child component definitions.
 */
export interface IComponentDef {
    type: string;
    components?: IComponentDef[];
}

/**
 * IRenderableComponent interface represents a renderable component built from a component definition.
 * @interface
 * @property {typeof SvelteComponent} type - The type of the component which should be a SvelteComponent.
 * @property {any} props - The properties of the component.
 */
export interface IRenderableComponent {
    type: typeof SvelteComponent;
    props: any;
    components?: IRenderableComponent[];
}

export interface IEventDef {
    type: string;
}

export interface GoToEvent extends IComponentDef {
    type: 'GoToEvent';
    url: string;
    query: Record<string, any> | null;
}



