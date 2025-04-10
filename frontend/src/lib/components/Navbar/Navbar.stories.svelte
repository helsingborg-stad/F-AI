<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Navbar from '$lib/components/Navbar/Navbar.svelte';

  const { Story } = defineMeta({
    title: 'Components/Navbar',
    component: Navbar,
    tags: ['autodocs'],
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
  name="Navbar title"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/settings',
	 	navbarTitle: 'My Navbar Title',
	}}
/>

<Story
  name="Avatar"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/settings',
	 	avatarUrl: 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp',
	 	avatarName: 'John Doe',
	 	navbarTitle: 'My Navbar Title',
	}}
/>

<Story
  name="Avatar placeholder"
  args={{
		navBarItems: sampleLinks,
		currentUrlPath: '/settings',
	 	avatarUrl: '',
	 	avatarPlaceholder: 'John Doe',
	 	navbarTitle: 'My Navbar Title',
	}}
/>

