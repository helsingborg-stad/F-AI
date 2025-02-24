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

<div class="root-layout">
	<header class="root-layout-header">
		<Navbar navbarTitle={NAVBAR_TITLE} {navBarItems} currentUrlPath={page.url.pathname} />
	</header>
	<div class="root-content">
		<aside class="root-content-aside">
			<MenuSidebar {menuSidebarItems} currentUrlPath={page.url.pathname} />
		</aside>
		<main class="root-content-main">
			{@render children()}
		</main>
	</div>
</div>

<style lang="postcss">
	@reference '../app.css';

	.root-layout {
		@apply h-screen flex flex-col;
	}

	.root-layout-header {
		@apply w-full bg-base-200 flex md:px-4;
	}

	.root-content {
		@apply flex flex-grow;
	}

	.root-content-aside {
		@apply flex-shrink-0 overflow-hidden bg-base-100 max-md:!w-0 w-60;
	}

	.root-content-main {
		@apply bg-stone-50 flex-grow;
	}
</style>
