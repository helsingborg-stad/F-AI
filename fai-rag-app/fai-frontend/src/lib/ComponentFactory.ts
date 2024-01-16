// ComponentFactory.ts

import type {SvelteComponent} from 'svelte';
import type {IComponentDef, IRenderableComponent} from './types';
import PageWithDrawer from './components/PageWithDrawer.svelte';
import Container from './components/Container.svelte';
import Heading from './components/Heading.svelte';
import Paragraph from './components/Paragraph.svelte';
import KcForm from "./components/KcForm.svelte";
import Page from "./components/Page.svelte";
import Div from "./components/Div.svelte";
import Form from "./components/Form.svelte";
import InputField from "./components/InputField.svelte";
import FireEvent from "./components/FireEvent.svelte";

const componentMap: Record<string, typeof SvelteComponent> = {
    PageWithDrawer,
    Container,
    Heading,
    Paragraph,
    KcForm,
    Page,
    Div,
    Form,
    InputField,
    FireEvent
};

function toRenderable({type, ...componentDef}: IComponentDef): IRenderableComponent {
    const Component = componentMap[type];
    if (!Component) {
        throw new Error(`No component found for type "${type}"`);
    }

    const children: IRenderableComponent[] = (componentDef.components || []).map(toRenderable);
    return {type: Component, props: {...componentDef, components: children}};
}

export default toRenderable;
