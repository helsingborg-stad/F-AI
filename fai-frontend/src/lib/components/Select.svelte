<script lang="ts">
  import { onMount } from 'svelte'
  import { FormControl } from '$lib/components/input'

  export let name: string
  export let title: string | null = null
  export let error: string | null = null
  export let placeholder: string = 'Choose an option'
  export let required: boolean | null = null
  export let id: string = name
  export let className: string | null = null
  export { className as class }
  export let value: string | null = null
  export let autocomplete: HTMLInputElement['autocomplete'] | null = null
  export let block: boolean | null = true
  export let variant: 'ghost' | 'bordered' = 'bordered'
  export let autoFocus: boolean | null = null

  export let readonly: boolean | null = null

  export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null

  export let label: string | null = null

  export let options:
    | [string, string, boolean | null][]
    | [string, string][]
    | [string][] = []

  let ref: HTMLInputElement

  onMount(() => autoFocus && ref?.focus() !== undefined)

  $: inputValue = ((v: string | null = null) => v)(value)
</script>

<FormControl
  {name}
  {size}
  {error}
  {label}
  class={readonly === true ? 'pointer-events-none' : null}
>
  <select
    class:select={true}
    class:select-ghost={variant === 'ghost'}
    class:select-bordered={variant === 'bordered'}
    class:w-full={block}
    class:select-xs={size === 'xs'}
    class:select-sm={size === 'sm'}
    class:select-md={size === 'md'}
    class:select-lg={size === 'lg'}
    class:select-error={error}
    on:input
    class={className}
    {id}
    {name}
    {required}
    bind:value={inputValue}
  >
    <option disabled selected value="">{placeholder}</option>

    {#each options as [v, label, disabled = null]}
      <option value={v} {disabled}>{label}</option>
    {/each}
  </select>
</FormControl>
