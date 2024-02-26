<script lang="ts">
    import {onMount} from 'svelte'

    export let name: string
    export let title: string | null = null
    export let error: string | null = null
    export let placeholder: string = "Choose an option";
    export let required: boolean | null = null;
    export let id: string = name;
    export let className: string | null = null;
    export {className as class};
    export let value: string | null = null;
    export let autocomplete: HTMLInputElement['autocomplete'] | null = null;
    export let block: boolean | null = true;
    export let variant: 'ghost' | 'bordered' = 'bordered'
    export let autoFocus: boolean | null = null;

    export let options: [string, string][] | [string][] = []

    let ref: HTMLInputElement;

    onMount(() => autoFocus && (ref?.focus() !== undefined))
</script>


<select
        class:select={true}
        class:select-ghost={variant === 'ghost'}
        class:select-bordered={variant === 'bordered'}
        class:w-full={block}
        class={className}
        id={id}
        name={name}
        required={required}

>
    <option disabled selected>{placeholder}</option>

    {#each options as [value, label]}
        <option value={value}>{label}</option>
    {/each}
</select>

{#if error}
    <div class="label label-text text-error mt-1">{error}</div>
{/if}




