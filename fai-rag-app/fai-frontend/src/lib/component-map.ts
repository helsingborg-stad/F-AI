import type {SvelteComponent} from "svelte";
import PageWithDrawer from "./components/PageWithDrawer.svelte";
import Container from "./components/Container.svelte";
import Heading from "./components/Heading.svelte";
import Paragraph from "./components/Paragraph.svelte";
import KcForm from "./components/KcForm.svelte";
import Page from "./components/Page.svelte";
import Div from "./components/Div.svelte";
import Form from "./components/Form.svelte";
import InputField from "./components/InputField.svelte";
import FireEvent from "./components/FireEvent.svelte";

export const componentMap: Record<string, typeof SvelteComponent> = {
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

export default componentMap