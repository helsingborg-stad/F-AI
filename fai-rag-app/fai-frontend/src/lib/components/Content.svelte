<script lang="ts">
  import { pageDataStore } from '$lib/store'
</script>

{#key $pageDataStore}
  <slot />
{/key}
