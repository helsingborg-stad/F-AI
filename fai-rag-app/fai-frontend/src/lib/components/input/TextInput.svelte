<script lang="ts">
  import { onMount } from 'svelte'
  import { FormControl, Input } from '$lib/components/input'

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

  export let disabled: boolean | null = null

  let ref: HTMLInputElement

  onMount(() => autoFocus && ref?.focus() !== undefined)

  $: inputValue = ((v: string | null = null) => v)(value)
</script>

<FormControl
  {name}
  {size}
  {error}
  {label}
  hidden={html_type === 'hidden'}
  class={readonly === true ? 'pointer-events-none' : null}
>
  <div
    class:font-normal={true}
    class:input={html_type !== 'hidden'}
    class:input-xs={size === 'xs' && html_type !== 'hidden'}
    class:input-sm={size === 'sm' && html_type !== 'hidden'}
    class:input-md={size === 'md' && html_type !== 'hidden'}
    class:input-lg={size === 'lg' && html_type !== 'hidden'}
    class:input-error={error}
    class:input-bordered={variant === 'bordered' && html_type !== 'hidden'}
    class:input-ghost={variant === 'ghost' && html_type !== 'hidden'}
    class:w-full={block}
    class:bg-base-200={readonly && html_type !== 'hidden'}
    class={'flex items-center space-x-3 ' + (className ?? '')}
    {disabled}
  >
    <slot name="prefix" />
    <Input
      class="max-h-full max-w-full grow"
      {name}
      {id}
      {placeholder}
      {readonly}
      {autocomplete}
      {required}
      type={html_type}
      bind:value={inputValue}
      on:input
      on:blur
      on:change
      on:focus
      {disabled}
    />
    <slot name="suffix" />
  </div>
</FormControl>
