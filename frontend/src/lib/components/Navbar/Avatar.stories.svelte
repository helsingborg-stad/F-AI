<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Avatar from '$lib/components/Navbar/Avatar.svelte'

  const { Story } = defineMeta({
    title: 'Components/Navbar/Avatar',
    component: Avatar,
    tags: ['autodocs'],
    parameters: {
      layout: 'centered', // This will center the component
    },
  })

  const menuItems = [
    {
      title: 'Logout',
      action: '',
    },
  ]
</script>

<Story name="Default" />

<Story
  name="With image"
  args={{
    avatarUrl:
      'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
  }}
/>

<Story
  name="With placeholder"
  args={{
    avatarPlaceholder: 'John Doe',
  }}
/>

<Story
  name="With menu"
  args={{
    avatarPlaceholder: 'John.Doe@mail.com',
    menuItems,
  }}
/>
