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
  <div
    class:font-normal={true}
    class:input={html_type !== 'hidden'}
    class:input-xs={size === 'xs'}
    class:input-sm={size === 'sm'}
    class:input-md={size === 'md'}
    class:input-lg={size === 'lg'}
    class:input-error={error}
    class:input-bordered={variant === 'bordered'}
    class:input-ghost={variant === 'ghost'}
    class:w-full={block}
    class={'flex items-center space-x-3 ' + (className ?? '')}
  >
    <slot name="prefix" />
    <Input
      class="max-h-full max-w-full grow"
      {name}
      {id}
      {placeholder}
      {readonly}
      {autocomplete}
      bind:value={inputValue}
      on:input
      on:blur
      on:change
      on:focus
    />
    <slot name="suffix" />
  </div>
</FormControl>
