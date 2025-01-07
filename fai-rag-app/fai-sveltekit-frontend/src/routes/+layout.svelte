<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores'

	import Navbar from '$lib/components/Navbar/Navbar.svelte';
	import MenuSidebar from '$lib/components/Menu/MenuSidebar.svelte';
</script>

<div class="h-screen">
	<div class="relative flex h-full overflow-hidden z-0">
		<MenuSidebar menuItems={[
				{label: 'Chat', path: '/chat'},
				{label: 'Questions', path: '/questions'},
				{label: 'Assistant', path: '/assistant'}
			]} currentUrlPath={$page.url.pathname} />
		<!-- Main Content -->
        <div class="relative flex h-full w-full flex-1 flex-col overflow-hidden">
            <!-- Header -->
            <div class="sticky top-0 z-10 w-full">
							<Navbar />
            </div>
            <!-- Page Content -->
					<div class="flex-1 flex flex-col bg-amber-50">
						<slot />
					</div>
        </div>
    </div>
</div>