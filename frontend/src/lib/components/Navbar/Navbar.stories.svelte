<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Navbar from '$lib/components/Navbar/Navbar.svelte';

  const { Story } = defineMeta({
    title: 'Components/Navbar',
    component: Navbar,
    tags: ['autodocs'],
    argTypes: {
      avatarUrl: { control: 'text' },
      avatarName: { control: 'text' },
      navBarItems: { control: 'array' },
      currentUrlPath: { control: 'text' }
    }
  });

  const sampleLinks = [
    {
      label: 'Some link 1',
      path: '/some_link_1'
    },
    {
      label: 'Some link 2',
      path: '/some_link_2'
    },
    {
      label: 'Settings',
      path: '/settings'
    }
  ];
</script>

<Story
  name="Default"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/settings',
	}}
/>

<Story
  name="Avatar"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/settings',
	 	avatarUrl: 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
	 	avatarName: 'John Doe',
	}}
/>

<Story
  name="Title"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/some_link_1',
	 	navbarTitle: 'My Navbar Title',
	}}
/>

<Story
  name="Title and Avatar"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/some_link_2',
	 	avatarUrl: 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
	 	avatarName: 'John Doe',
	 	navbarTitle: 'My Navbar Title',
	}}
/>
