import type { SvelteComponent } from 'svelte'
import Heading from '$lib/components/Heading.svelte'
import Div from '$lib/components/Div.svelte'
import Form from '$lib/components/Form.svelte'
import { TextInput as InputField } from '$lib/components/input'
import FireEvent from '$lib/components/FireEvent.svelte'
import AppShell from '$lib/components/AppShell.svelte'
import AppDrawer from '$lib/components/AppDrawer.svelte'
import AppContent from '$lib/components/AppContent.svelte'
import Divider from '$lib/components/Divider.svelte'
import AppFooter from '$lib/components/AppFooter.svelte'
import Dropdown from '$lib/components/Dropdown.svelte'
import Link from '$lib/components/Link.svelte'
import Menu from '$lib/components/Menu.svelte'
import Button from '$lib/components/Button.svelte'
import Textarea from '$lib/components/Textarea.svelte'
import Table from '$lib/components/Table.svelte'
import type { DataTable } from '$lib/components/table'
import Pagination from '$lib/components/Pagination.svelte'
import ChatBubble from '$lib/components/ChatBubble.svelte'
import Select from '$lib/components/Select.svelte'
import Radio from '$lib/components/Radio.svelte'
import SSEChat from '$lib/components/chat/SSEChat.svelte'
import FileInput from '$lib/components/FileInput.svelte'
import PageHeader from './components/AppHeader.svelte'
import PageContent from './components/Content.svelte'
import Text from '$lib/components/Text.svelte'
import Range from '$lib/components/Range.svelte'

type addPrefixToObject<T, P extends string> = {
  [K in keyof T as K extends string ? `${P}${K}` : never]: T[K]
}

/**
 * IComponentDef interface represents a base component definition (fetched from server as json).
 * @interface
 * @property {ComponentType} type - The type of the component.
 * @property {IComponentDef[]} [components] - The optional array of child component definitions.
 */
export interface IComponentDef {
  type: ComponentType
  components?: IComponentDef[]
  slot?: IComponentDef[] | IComponentDef

  [key: string]:
    | any
    | addPrefixToObject<IComponentDef[] | IComponentDef, 'slot.'>
    | addPrefixToObject<IComponentDef[] | IComponentDef, 'on:'>
}

/**
 * IRenderableComponent interface represents a renderable component built from a component definition.
 * @interface
 * @property {typeof SvelteComponent} type - The type of the component which should be a SvelteComponent.
 * @property {any} props - The properties of the component.
 */
export interface IRenderableComponent {
  component: SvelteComponentDef
  type: SvelteComponentDef
  props: any
  components?: IRenderableComponent[]

  slots?: Record<string, IRenderableComponent[]>
  events?: Record<string, (e: AnyEvent) => void>
}

export type ComponentsMap = {
  Heading: typeof Heading
  Div: typeof Div
  Form: typeof Form
  InputField: typeof InputField
  FireEvent: typeof FireEvent
  AppShell: typeof AppShell
  AppDrawer: typeof AppDrawer
  AppContent: typeof AppContent
  AppFooter: typeof AppFooter
  PageHeader: typeof PageHeader
  PageContent: typeof PageContent
  Dropdown: typeof Dropdown
  Link: typeof Link
  Menu: typeof Menu
  Button: typeof Button
  Textarea: typeof Textarea
  Text: typeof Text
  Table: typeof Table
  DataTable: typeof DataTable
  Pagination: typeof Pagination
  ChatBubble: typeof ChatBubble
  Select: typeof Select
  Radio: typeof Radio
  SSEChat: typeof SSEChat
  FileInput: typeof FileInput
  Divider: typeof Divider
  Range: typeof Range
}

export type ComponentType = keyof ComponentsMap

export type SvelteComponentDef = ComponentsMap[ComponentType]

export enum EventType {
  GoTo = 'GoToEvent',
}

export interface IEventDef {
  type: EventType
}

export interface GoToEventProps {
  url: string
  query: Record<string, any> | null
}

export interface GoToEvent extends IEventDef, GoToEventProps {
  type: EventType.GoTo
}

export interface EventToHandlerMap {
  [EventType.GoTo]: ({ url, query }: GoToEventProps) => void
}

export type AnyEvent = GoToEvent
