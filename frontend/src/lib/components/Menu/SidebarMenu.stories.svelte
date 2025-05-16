<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/SidebarMenu',
    component: SidebarMenu,
    tags: ['autodocs'],
    argTypes: {
      title: { control: 'object' },
    },
  })
</script>
<script>
  import MenuLinkList from '$lib/components/Menu/MenuLinkList.svelte'
</script>

<Story name="Default" args={{title: 'My Menu'}}>
  <div class="px-4">
    <p>My menu content</p>
    <p>My menu content</p>
    <p>My menu content</p>
  </div>
</Story>

<Story name="Link List" args={{ title: "Link list example"}}>
  <MenuLinkList
    items={[
    { label: 'Cool Link A', path: '/A'},
    { label: 'Cool Link B', path: '/B'},
    { label: 'Cool Link C', path: '/C'},
  ]}
    activePath={'/A'}
  />
</Story>