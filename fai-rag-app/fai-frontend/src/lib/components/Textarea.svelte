<script lang="ts">

    export let className: string | null = null
    export {className as class}
    export let name: string
    export let id: string = name
    export let title: string | null = null
    export let variant: 'ghost' | 'bordered' | null = 'bordered'
    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let rows: number | null = null
    export let cols: number | null = null
    export let error: string | null = null
    export let placeholder: string | null = null
    export let required: boolean | null = null;
    export let disabled: boolean | null = null;
    export let readonly: boolean | null = null;
    export let value: string | null = null;
    export let autocomplete: HTMLInputElement['autocomplete'] | null = null;
</script>

<div
        class:form-control={1}>
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
        class:textarea-bordered={variant === 'bordered'}
        class:textarea-ghost={variant === 'ghost'}
        class:textarea-warning={state === 'warning'}
        class:textarea-success={state === 'success'}
        class:textarea-info={state === 'info'}
        class:textarea-accent={state === 'accent'}
        class:textarea-primary={state === 'primary'}
        class:textarea-secondary={state === 'secondary'}
        class:textarea-error={error || (state === 'error')}
        class:w-full={true}
        class={className}></textarea>
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</div>


