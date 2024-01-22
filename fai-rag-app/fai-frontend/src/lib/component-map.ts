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
import Dropdown from "./components/Dropdown.svelte";
import Link from "./components/Link.svelte";
import Menu from "./components/Menu.svelte";
import AppShell from "./components/AppShell.svelte";
import AppDrawer from "./components/AppDrawer.svelte";
import AppContent from "./components/AppContent.svelte";
import AppFooter from "./components/AppFooter.svelte";
import PageHeader from "./components/PageHeader.svelte";
import PageContent from "./components/PageContent.svelte";
import Button from "./components/Button.svelte";
import Textarea from "./components/Textarea.svelte";

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
    FireEvent,
    Dropdown,
    Link,
    Menu,
    AppShell,
    AppDrawer,
    AppContent,
    AppFooter,
    PageHeader,
    PageContent,
    Button
};

export default componentMap