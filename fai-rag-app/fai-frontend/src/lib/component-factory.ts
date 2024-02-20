// ComponentFactory.ts

import type {IComponentDef, IRenderableComponent} from './types';
import componentsMap from "./component-map";

const normalizeSlotKey = (slotName: string) => slotName === 'slot' ? 'default' : slotName.replace('slot.', '');
const normalize2Array = (value: any) => Array.isArray(value) ? value : [value];

function toRenderable(componentDefOrRenderable: IComponentDef | IRenderableComponent): IRenderableComponent {
    if (typeof (componentDefOrRenderable as IRenderableComponent).type !== 'string')
        return componentDefOrRenderable as IRenderableComponent

    const {type, ...rest} = componentDefOrRenderable as IComponentDef;

    // reduce to segregate properties based on 'slot' and 'on:' prefixes
    const {slots, events, props} = Object.keys(rest).reduce((acc, key) => {
        const matchers =
            [
                [() => key.startsWith('slot'), () => acc.slots[normalizeSlotKey(key)] = normalize2Array(acc.slots[key]).map(toRenderable)],
                [() => key.startsWith('on:'), () => acc.events[key] = rest[key]],
                [() => key.startsWith('renderProps.'), () => acc.props[key.replace('renderProps.', '')] = normalize2Array(rest[key]).map(toRenderable)],
                [() => true, () => acc.props[key] = rest[key]]

            ]

        const [matcher, action] = matchers.find(([matcher]) => matcher()) || [() => false, () => {
        }]
        action()
        return acc
    }, {
        slots: {} as Record<string, IRenderableComponent[]>,
        events: {} as { [key: string]: any },
        props: {} as { [key: string]: any }
    });


    const Component = componentsMap[type]


    if (!Component)
        throw new Error(`No component found for type "${type}"`)


    return {
        component: Component,
        type: Component,
        props: {
            ...props,
        },
        slots,
        events
    }
}

export default toRenderable;
