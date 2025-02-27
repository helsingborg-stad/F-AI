<script lang="ts">
  import { page } from '$app/state'
  import '../app.css'

  let { children } = $props()

  const area = page.url.pathname.startsWith('/login') ? 'public' : 'app'
</script>

{#key area}
  {@render children()}
{/key}
