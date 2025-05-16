<script module>
  import { fn } from '@storybook/test'
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import MenuHeader from '$lib/components/Menu/MenuHeader.svelte'

  const { Story } = defineMeta({
    title: 'Components/Menu/MenuHeader',
    component: MenuHeader,
    tags: ['autodocs'],
    argTypes: {
      title: { control: 'text' },
      iconName: {
        control: 'select',
        options: ['panelLeft', 'banana'],
      },
    },
  })
</script>

<Story name="Default" args={{ title: "Chat", iconName: "panelLeft", onClick: fn() }} />