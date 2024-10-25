<script lang="ts">
  import { FormControl, Input } from '$lib/components/input'
  export let className: string | null = null
  export { className as class }
  export let name: string
  export let id: string = name
  export let title: string | null = null
  export let variant: 'ghost' | 'bordered' | null = 'bordered'
  export let state:
    | 'primary'
    | 'secondary'
    | 'accent'
    | 'success'
    | 'info'
    | 'warning'
    | 'error'
    | null = null
  export let rows: number | null = null
  export let cols: number | null = null
  export let error: string | null = null
  export let placeholder: string | null = null
  export let required: boolean | null = null
  export let disabled: boolean | null = null
  export let readonly: boolean | null = null
  export let value: string | null = null
  export let autocomplete: HTMLInputElement['autocomplete'] | null = null

  export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
  export let block: boolean | null = true
  export let autoFocus: boolean | null = null

  export let inputValue: string = value ?? ''

  export let label: string | null = null
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
    class:w-full={block}
    class={'flex items-center space-x-3 ' + (className ?? '')}
    {disabled}
  >
    <slot name="prefix" />
    <textarea
      {name}
      {id}
      {title}
      {placeholder}
      {required}
      {value}
      {autocomplete}
      {rows}
      {cols}
      {disabled}
      {readonly}
      class:textarea={true}
      class:textarea-xs={size === 'xs'}
      class:textarea-sm={size === 'sm'}
      class:textarea-md={size === 'md'}
      class:textarea-lg={size === 'lg'}
      class:textarea-bordered={variant === 'bordered'}
      class:textarea-ghost={variant === 'ghost'}
      class:textarea-warning={state === 'warning'}
      class:textarea-success={state === 'success'}
      class:textarea-info={state === 'info'}
      class:textarea-accent={state === 'accent'}
      class:textarea-primary={state === 'primary'}
      class:textarea-secondary={state === 'secondary'}
      class:textarea-error={error || state === 'error'}
      class:w-full={true}
      class={className}
    />
    <slot name="suffix" />
  </div>
</FormControl>
