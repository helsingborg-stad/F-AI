<script lang="ts">
  import type { Action } from 'svelte/action'

  export let name: string
  export let placeholder: string | null = null
  export let required: boolean | null = null
  export let id: string = name
  export let className: string | null = null
  export { className as class }
  export let html_type: 'text' | 'password' | 'hidden' | 'number' | 'email' | 'tel' =
    'text'
  export { html_type as type }
  export let value: string | null = null
  export let autocomplete: HTMLInputElement['autocomplete'] | null = null
  export let autoFocus: boolean | null = null

  export let readonly: boolean | null = null

  const focusOnMount: Action<HTMLInputElement, boolean | null> = (node, focus) => {
    focus === true && node.focus()
  }

  $: inputValue = ((v: string | null = null) => v)(value)
</script>

<input
  class={className ?? null}
  type={html_type}
  value={inputValue}
  class:hidden={html_type === 'hidden'}
  class:mt-0={html_type === 'hidden'}
  on:input
  on:change
  on:blur
  on:focus
  {name}
  {id}
  {placeholder}
  {required}
  {autocomplete}
  {readonly}
  {...$$restProps}
  use:focusOnMount={autoFocus}
/>
