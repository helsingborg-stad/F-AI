// ComponentFactory.ts

import type {IComponentDef, IRenderableComponent} from './types';
import components from "./component-map";

function toRenderable({type, ...componentDef}: IComponentDef): IRenderableComponent {
    const Component = components[type];
    if (!Component) {
        throw new Error(`No component found for type "${type}"`);
    }

    const children: IRenderableComponent[] = (componentDef.components || []).map(toRenderable);
    return {type: Component, props: {...componentDef, components: children}};
}

export default toRenderable;
