<script lang="ts">
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    title: string
    onRemove: () => void
    state: 'valid' | 'invalid' | 'pending'
    maxTitleLength?: number
  }

  const { title, onRemove, state, maxTitleLength = 15 }: Props = $props()

  const shortTitle = $derived(
    title.length > maxTitleLength ? title.slice(0, maxTitleLength - 3) + '...' : title,
  )
</script>

<div
  class="group relative flex max-w-fit rounded-lg border border-gray-200 p-1"
  class:bg-red-600={state === 'invalid'}
  class:opacity-50={state === 'pending'}
>
  <div class="flex items-center gap-1 rounded">
    <!-- Icon -->
    <div
      class="flex h-8 w-8 items-center justify-center rounded"
      class:bg-red-500={state === 'invalid'}
      class:bg-gray-500={state === 'pending'}
    >
      {#if state === 'invalid'}
        <img
          alt="invalid"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNpcmNsZS14Ij48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIvPjxwYXRoIGQ9Im0xNSA5LTYgNiIvPjxwYXRoIGQ9Im05IDkgNiA2Ii8+PC9zdmc+"
        />
      {:else if state === 'pending'}
        <img
          alt="pending"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWVsbGlwc2lzIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxIi8+PGNpcmNsZSBjeD0iMTkiIGN5PSIxMiIgcj0iMSIvPjxjaXJjbGUgY3g9IjUiIGN5PSIxMiIgcj0iMSIvPjwvc3ZnPg=="
        />
      {:else}
        <img
          alt="valid"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWZpbGUtdGV4dCI+PHBhdGggZD0iTTE1IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY3WiIvPjxwYXRoIGQ9Ik0xNCAydjRhMiAyIDAgMCAwIDIgMmg0Ii8+PHBhdGggZD0iTTEwIDlIOCIvPjxwYXRoIGQ9Ik0xNiAxM0g4Ii8+PHBhdGggZD0iTTE2IDE3SDgiLz48L3N2Zz4="
        />
      {/if}
    </div>

    <!-- Text -->
    <span class="mr-6 break-keep">{shortTitle}</span>

    <!-- Button -->
    {#if state !== 'pending'}
      <button
        class="invisible absolute -right-0 -top-0 rounded-full bg-gray-100 p-1 hover:bg-gray-300 active:bg-gray-500 group-hover:visible"
        onclick={onRemove}
      >
        <Icon icon={icons.trash} width={16} height={16} />
      </button>
    {/if}
  </div>
</div>
