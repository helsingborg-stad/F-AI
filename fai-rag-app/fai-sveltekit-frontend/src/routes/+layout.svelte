<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte';
	import Navbar from '$lib/components/Navbar/Navbar.svelte';

	let { children } = $props();

	const NAVBAR_TITLE = 'Folkets AI';

	const navBarItems = [
		{ label: 'Chat', path: '/chat' },
		{ label: 'Settings', path: '/settings' }
	];

	const menuSidebarItems = [
		{ label: 'Home', path: '/' },
		{ label: 'Hello', path: '/hello' },
		{ label: 'Chat', path: '/chat' },
		{ label: 'Assistant', path: '/assistant' }
	];
</script>

<div class="h-screen flex flex-col">
	<nav class="w-full bg-blue-100 flex md:px-4">
		<Navbar navbarTitle={NAVBAR_TITLE} {navBarItems} currentUrlPath={page.url.pathname} />
	</nav>
	<div class="flex flex-grow">
		<aside class="w-48 h-full p-4">
			<MenuSidebar {menuSidebarItems} currentUrlPath={page.url.pathname} />
		</aside>
		<main class="bg-amber-100 flex-grow h-auto p-4">
			{@render children()}
		</main>
	</div>
</div>
