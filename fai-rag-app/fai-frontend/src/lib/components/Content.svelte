<script lang="ts">
  import { path, searchParams, url } from 'elegua'
</script>

{#key $url}
  <slot />
{/key}
