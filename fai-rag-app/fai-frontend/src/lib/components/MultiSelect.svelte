<script lang="ts">
    import {createEventDispatcher} from 'svelte'
    import {writable} from "svelte/store";

    const dispatch = createEventDispatcher();
    export let name: string
    export let title: string | null = null
    export let error: string | null = null
    export let placeholder: string = "Choose an option";
    export let required: boolean | null = null;
    export let id: string = name;
    export let className: string | null = null;
    export {className as class};
    export let value: string[] = [];

    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null;

    export let initialValue: string[] | null = null;
    export let block: boolean | null = true;
    export let variant: 'ghost' | 'bordered' = 'bordered'
    export let autoFocus: boolean | null = null;

    export let options: [string, string, boolean | null][] | [string, string][] | [string][] = []


    let selectedValues = writable<string[]>(initialValue ?? [])
    $: $selectedValues = value
    $: dispatch('inputChange', $selectedValues)
</script>

<select
        class:select={true}
        class:select-ghost={variant === 'ghost'}
        class:select-bordered={variant === 'bordered'}
        class:w-full={block}
        class:select-primary={state === 'primary'}
        class:select-secondary={state === 'secondary'}
        class:select-accent={state === 'accent'}
        class:select-success={state === 'success'}
        class:select-info={state === 'info'}
        class:select-warning={state === 'warning'}
        class:select-error={state === 'error'}
        
        class={className}
        id={id}
        name={name}
        required={required}
        multiple
        bind:value={$selectedValues}

>
    <option disabled selected value="">{placeholder}</option>

    {#each options as [v, label, disabled = null]}
        <option value={v} {disabled}>{label}</option>
    {/each}
</select>

{#if error}
    <div class="label label-text text-error mt-1">{error}</div>
{/if}




