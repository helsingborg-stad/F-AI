<script lang="ts">
    import {writable} from 'svelte/store';

    export let className: string | null;
    export {className as class};
    export let name: string;
    export let id: string = name;
    export let title: string | null = null;
    export let error: string | null = null;
    export let placeholder: string | null = null;
    export let required: boolean | null = null;
    export let html_type: 'text' | 'password' | 'hidden' | 'number' | 'email' | 'tel' = 'text';
    export let value: string | undefined = undefined;
    export let hidden: boolean | null = null;
    export let autocomplete: HTMLInputElement['autocomplete'] | null = null;

    let attributes = writable({});
    $: $attributes = {

        name,
        id,
        title,
        placeholder,
        required,
        type: html_type,
        value,
        autocomplete,
        hidden,
        error
    }
</script>

<div class:hidden={html_type === 'hidden'} class:mt-0={html_type === 'hidden'}>
    <input class={['input', 'input-bordered', 'w-full', className].filter(c => c).join(' ')}
           class:input-error={error}
           {...$attributes}/>
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</div>



