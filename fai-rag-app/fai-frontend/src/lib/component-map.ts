import type {SvelteComponent} from "svelte";
import Heading from "./components/Heading.svelte";
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
import PageHeader from "./components/AppHeader.svelte";
import PageContent from "./components/Content.svelte";
import Button from "./components/Button.svelte";
import Textarea from "./components/Textarea.svelte";
import Text from "./components/Text.svelte";
import Table from "./components/Table.svelte";
import Pagination from "./components/Pagination.svelte";
import ChatBubble from "./components/ChatBubble.svelte";
import Select from "./components/Select.svelte";
import FileInput from "./components/FileInput.svelte";


export const componentMap: Record<string, typeof SvelteComponent> = {
    Heading,
    Div,
    Form,
    InputField,
    FireEvent,
    AppShell,
    AppDrawer,
    AppContent,
    AppFooter,
    PageHeader,
    PageContent,
    Dropdown,
    Link,
    Menu,
    Button,
    Textarea,
    Text,
    Table,
    Pagination,
    ChatBubble,
    Select,
    FileInput
}

export default componentMap