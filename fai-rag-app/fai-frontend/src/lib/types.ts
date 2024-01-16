import type {SvelteComponent} from "svelte";

export interface IComponentDef {
    type: string;
    className?: string;
    components?: IComponentDef[];
}

export interface IEventDef {
    type: string;
}

export interface GoToEvent extends IComponentDef {
    type: 'GoToEvent';
    url: string;
    query: Record<string, any> | undefined | null;
}

export interface IRenderableComponent {
    type: typeof SvelteComponent;
    props: any;
}

