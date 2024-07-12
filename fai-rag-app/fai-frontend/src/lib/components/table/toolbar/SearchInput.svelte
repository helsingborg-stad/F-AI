<script lang="ts">
  import SVG from '$lib/components/SVG.svelte'
  import { TextInput } from '$lib/components/input'
  import Button from '$lib/components/Button.svelte'

  export let filterValue: string | null = null

  export let resetHandler: () => any

  $: value = filterValue
  $: showClearButton = value !== null && value !== ''
</script>

<TextInput
  class="join-item max-w-xs text-sm font-medium {value !== (null || '')
    ? 'border-neutral text-neutral outline-1 focus:outline-neutral'
    : ''}"
  name="search"
  html_type="search"
  bind:value
  on:input
  placeholder="Search all data..."
>
  <SVG
    slot="prefix"
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlYXJjaCI+PGNpcmNsZSBjeD0iMTEiIGN5PSIxMSIgcj0iOCIvPjxwYXRoIGQ9Im0yMSAyMS00LjMtNC4zIi8+PC9zdmc+"
  />

  <svelte:fragment slot="suffix">
    {#key showClearButton}
      <Button
        size="sm"
        circle
        variant="ghost"
        class={!showClearButton ? 'opacity-0' : null}
        disabled={!showClearButton}
        on:click={resetHandler}
      >
        <SVG
          src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXgiPjxwYXRoIGQ9Ik0xOCA2IDYgMTgiLz48cGF0aCBkPSJtNiA2IDEyIDEyIi8+PC9zdmc+"
        />
      </Button>
    {/key}
  </svelte:fragment>
</TextInput>
