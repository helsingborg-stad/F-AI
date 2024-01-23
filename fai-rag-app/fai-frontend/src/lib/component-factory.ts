// ComponentFactory.ts

import type {IComponentDef, IRenderableComponent} from './types';
import componentsMap from "./component-map";


function toRenderable(componentDefOrRenderable: IComponentDef | IRenderableComponent): IRenderableComponent {
    if ("props" in componentDefOrRenderable)
        return componentDefOrRenderable

    const {type, components, ...props} = componentDefOrRenderable

    const Component = componentsMap[type]

    if (!Component)
        throw new Error(`No component found for type "${type}"`)


    const children: IRenderableComponent[] = (components || []).map(toRenderable)
    return {
        type: Component, props: {
            ...props,
            ...(children.length > 0 ? {components: children} : {})
        }
    }
}

export default toRenderable;
