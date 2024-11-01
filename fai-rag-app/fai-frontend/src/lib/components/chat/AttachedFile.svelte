<script lang="ts">
  import SVG from '$lib/components/SVG.svelte'

  export let title: string
  export let onRemove: () => void
  export let state: 'valid' | 'invalid' | 'pending'

  const maxTitleLength = 15

  $: shortTitle = title.length > maxTitleLength ? title.slice(0, maxTitleLength - 3) + '...' : title

</script>

<div class="p-1">
  <div
    class="flex items-center gap-2 p-2 bg-gray-800 text-white rounded relative"
    class:bg-red-600={state === 'invalid'}
    class:opacity-50={state === 'pending'}
  >
    <div
      class="bg-orange-500 rounded w-8 h-8 flex items-center justify-center"
      class:bg-red-500={state === 'invalid'}
      class:bg-gray-500={state === 'pending'}
    >
      {#if state === 'invalid'}
        <SVG
          width="24"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNpcmNsZS14Ij48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIvPjxwYXRoIGQ9Im0xNSA5LTYgNiIvPjxwYXRoIGQ9Im05IDkgNiA2Ii8+PC9zdmc+"
        />
      {:else if state === 'pending'}
        <SVG
          width="24"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWVsbGlwc2lzIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxIi8+PGNpcmNsZSBjeD0iMTkiIGN5PSIxMiIgcj0iMSIvPjxjaXJjbGUgY3g9IjUiIGN5PSIxMiIgcj0iMSIvPjwvc3ZnPg=="
        />
      {:else}
        <SVG
          width="24"
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWZpbGUtdGV4dCI+PHBhdGggZD0iTTE1IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY3WiIvPjxwYXRoIGQ9Ik0xNCAydjRhMiAyIDAgMCAwIDIgMmg0Ii8+PHBhdGggZD0iTTEwIDlIOCIvPjxwYXRoIGQ9Ik0xNiAxM0g4Ii8+PHBhdGggZD0iTTE2IDE3SDgiLz48L3N2Zz4="
        />
      {/if}
    </div>
    <span class="break-keep">{shortTitle}</span>
    <button
      on:click={onRemove}
      class="absolute -right-1 -top-1 w-5 h-5 bg-black text-xs flex items-center justify-center rounded-full"
    >
      X
    </button>
  </div>
</div>