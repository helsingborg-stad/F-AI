<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte';

  const { Story } = defineMeta({
    title: 'Components/Menu/MenuSidebar',
    component: MenuSidebar,
    tags: ['autodocs'],
    argTypes: {
      menuSidebarItems: { control: 'object' },
      currentUrlPath: { control: 'text' },
    },
  });

  const sampleMenuItems = [
    { label: 'Home', path: '/' },
    { label: 'About', path: '/about' },
    { label: 'Contact', path: '/contact' },
  ];
</script>

<!-- Sidebar will be hidden for smaller screens. -->
<Story name="Default" args={{ menuSidebarItems: sampleMenuItems, currentUrlPath: '/' }} />

<!-- Story with 'About' page active. -->
<Story name="About Page Active" args={{ menuSidebarItems: sampleMenuItems, currentUrlPath: '/about' }} />
