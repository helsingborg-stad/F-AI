<script>
	import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte';

	let { children } = $props();

	let menuSidebarItems = [{
		label: 'Asistant Zoo',
		path: ''
	}]
</script>

<MenuSidebar {menuSidebarItems} />

{@render children()}
