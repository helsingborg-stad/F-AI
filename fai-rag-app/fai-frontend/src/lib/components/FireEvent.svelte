<script lang="ts">
  import { onMount } from 'svelte'
  import type { GoToEvent } from '../types'
  import { goto } from 'elegua'

  export let event: GoToEvent

  const events = {
    GoToEvent: ({
      url,
      query,
    }: {
      url: string
      query: Record<string, any> | null | null
    }) => {
      console.log('trying to go to', url, query)
      goto(url + (query ? '?' + new URLSearchParams(query).toString() : ''))
    },
  }

  const { type, ...props } = event
  onMount(() => (events[type] || (() => null))(props))
</script>
