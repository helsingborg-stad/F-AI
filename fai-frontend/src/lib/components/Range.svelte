<script lang="ts">
  import type { Action } from 'svelte/action'
  import { onMount } from 'svelte'
  import { FormControl, Input, Label } from '$lib/components/input'
  export let name: string
  export let label: string | null = null
  export let error: string | null = null
  export let placeholder: string | null = null
  export let required: boolean | null = null
  export let id: string = name
  export let className: string | null = null
  export { className as class }
  export let html_type:
    | 'text'
    | 'password'
    | 'hidden'
    | 'number'
    | 'email'
    | 'tel'
    | 'search' = 'text'

  export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
  export let value: string | null = null
  export let autocomplete: HTMLInputElement['autocomplete'] | null = null
  export let block: boolean | null = true
  export let variant: 'ghost' | 'bordered' = 'bordered'
  export let autoFocus: boolean | null = null
  export let readonly: boolean | null = null

  export let min: number | null = null
  export let max: number | null = null

  export let step: number | null = null

  export let disabled: boolean | null = null

  let ref: HTMLInputElement

  const focusOnMount: Action<HTMLInputElement, boolean | null> = (node, focus) => {
    focus === true && node.focus()
  }

  $: inputValue = ((v: string | null = null) => v)(value)
</script>

<FormControl
  {name}
  {size}
  {error}
  {label}
  class={readonly === true ? 'pointer-events-none' : null}
>
  <svelte:fragment slot="label">
    {#if label !== null}
      <Label altText={inputValue}>{label}</Label>
    {/if}
  </svelte:fragment>
  <input
    class={className ?? null}
    type="range"
    bind:value={inputValue}
    class:hidden={html_type === 'hidden'}
    class:mt-0={html_type === 'hidden'}
    class:range={1}
    class:range-xs={size === 'xs'}
    class:range-sm={size === 'sm'}
    class:range-md={size === 'md'}
    class:range-lg={size === 'lg'}
    on:input
    on:change
    on:blur
    on:focus
    {min}
    {max}
    {step}
    {name}
    {id}
    {placeholder}
    {required}
    {autocomplete}
    {readonly}
    class:bg-base-200={readonly && html_type !== 'hidden'}
    {...$$restProps}
    use:focusOnMount={autoFocus}
  />
</FormControl>
