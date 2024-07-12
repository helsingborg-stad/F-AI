<script lang="ts">
  import { onMount } from 'svelte'
  import type { AnyEvent } from '../types'
  import { eventToHandlerMap } from '$lib/event'

  export let event: AnyEvent

  const { type, ...props } = event
  onMount(() => eventToHandlerMap[type](props))
</script>
