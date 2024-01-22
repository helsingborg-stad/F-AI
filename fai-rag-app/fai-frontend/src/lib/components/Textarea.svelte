<script lang="ts">
    import {writable} from 'svelte/store';

    export let className: string | null;
    export {className as class};
    export let name: string;
    export let id: string = name;
    export let error: string | null = null;
    export let placeholder: string | null = null;
    export let required: boolean | null = null;
    export let disabled: boolean | null = null;
    export let readonly: boolean | null = null;
    export let variant: 'ghost' | 'bordered' | null = 'bordered'
    export let rows: number | null = null
    export let cols: number | null = null
    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let value: string | undefined = undefined;
    export let hidden: boolean | null = null;
    export let autocomplete: HTMLInputElement['autocomplete'] | null = null;

    let attributes = writable({});
    $: $attributes = {
        class: className,
        name,
        id,
        placeholder,
        required,
        value,
        autocomplete,
        hidden,
        error,
        rows,
        cols,
        disabled,
        readonly
    }
</script>

<div>
    <textarea
            class:textarea={true}
            class:textarea-bordered={variant === 'bordered'}
            class:textarea-ghost={variant === 'ghost'}
            class:textarea-error={state === 'error' || error}
            class:textarea-warning={state === 'warning'}
            class:textarea-success={state === 'success'}
            class:textarea-info={state === 'info'}
            class:textarea-accent={state === 'accent'}
            class:textarea-primary={state === 'primary'}
            class:textarea-secondary={state === 'secondary'}
            class:w-full={true}
            {...$attributes}></textarea>
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</div>



