<script lang="ts">
  import SidebarMenu from '$lib/components/Menu/SidebarMenu.svelte'
  import ResponsiveSidebar from '$lib/components/Menu/Chat/ResponsiveSidebar.svelte'

  let { children } = $props()
</script>

<div class="flex bg-base-200 h-full overflow-hidden relative">
  <ResponsiveSidebar>
    <SidebarMenu title="Settings" />
  </ResponsiveSidebar>
  <main class="m-2 flex-grow rounded-lg border bg-stone-50">
    {@render children()}
  </main>
</div>
