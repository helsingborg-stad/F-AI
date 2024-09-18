import type { SvelteComponent } from 'svelte'
import Heading from './components/Heading.svelte'
import Div from './components/Div.svelte'
import Form from './components/Form.svelte'
import InputField from './components/InputField.svelte'
import FireEvent from './components/FireEvent.svelte'
import Dropdown from './components/Dropdown.svelte'
import Link from './components/Link.svelte'
import Menu from './components/Menu.svelte'
import AppShell from './components/AppShell.svelte'
import AppDrawer from './components/AppDrawer.svelte'
import AppContent from './components/AppContent.svelte'
import AppFooter from './components/AppFooter.svelte'
import PageHeader from './components/AppHeader.svelte'
import PageContent from './components/Content.svelte'
import Button from './components/Button.svelte'
import Textarea from './components/Textarea.svelte'
import Text from './components/Text.svelte'
import Table from './components/Table.svelte'
import { DataTable } from '$lib/components/table'
import Pagination from './components/Pagination.svelte'
import ChatBubble from './components/ChatBubble.svelte'
import Select from './components/Select.svelte'
import Radio from './components/Radio.svelte'
import FileInput from './components/FileInput.svelte'
import SSEChat from './components/SSEChat.svelte'
import Divider from './components/Divider.svelte'
import type { ComponentsMap } from '$lib/types'
import Range from './components/Range.svelte'

export const componentMap: ComponentsMap = {
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
  DataTable,
  Pagination,
  ChatBubble,
  Select,
  Radio,
  SSEChat,
  FileInput,
  Range,
  Divider,
}

export default componentMap
