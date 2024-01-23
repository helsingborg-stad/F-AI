<script lang="ts">
    import {onMount} from 'svelte'

    export let name: string
    export let title: string | null = null
    export let error: string | null = null
    export let placeholder: string | null = null;
    export let required: boolean | null = null;
    export let id: string = name;
    export let className: string | null = null;
    export {className as class};
    export let html_type: 'text' | 'password' | 'hidden' | 'number' | 'email' | 'tel' = 'text';
    export let value: string | null = null;
    export let autocomplete: HTMLInputElement['autocomplete'] | null = null;
    export let block: boolean | null = true;
    export let variant: 'ghost' | 'bordered' = 'bordered'
    export let autoFocus: boolean | null = null;

    let ref: HTMLInputElement;

    onMount(() => autoFocus && (ref?.focus() !== undefined))
</script>

<div
        class:hidden={html_type === 'hidden'}
        class:mt-0={html_type === 'hidden'}>
    <input
            bind:this={ref}
            class:input={html_type !== 'hidden'}
            class:input-error={error}
            class:input-bordered={variant === 'bordered'}
            class:input-ghost={variant === 'ghost'}
            class:w-full={block}
            class={className ?? null}
            type={html_type},
            {name}
            {id}
            {title}
            {placeholder}
            {required}
            {value}
            {autocomplete}

    />
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</div>



