<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import MenuLinkList from '$lib/components/Menu/MenuLinkList.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/MenuLinkList',
    component: MenuLinkList,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={{
  items: [
    { label: 'Cool Link A', path: '/A'},
    { label: 'Cool Link B', path: '/B'},
    { label: 'Cool Link C', path: '/C'},
  ],
  activePath: '/A'
}} />