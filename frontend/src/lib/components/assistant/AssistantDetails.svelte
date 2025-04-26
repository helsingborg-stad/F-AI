<script lang="ts">
  import type { IAssistant } from '$lib/types.js'

  interface Props {
    assistant?: IAssistant
  }

  let { assistant }: Props = $props()
</script>

{#if assistant}
  <p>Assistant details</p>
{/if}