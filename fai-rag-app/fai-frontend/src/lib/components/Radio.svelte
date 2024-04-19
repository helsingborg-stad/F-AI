<script lang="ts">
    import {onMount} from 'svelte'
    import Text from "./Text.svelte";

    export let name: string
    export let title: string | null = null
    export let error: string | null = null
    export let required: boolean | null = null;
    export let options: [string, string][] | [string][] = []
    export let autoFocus: boolean | null = null;

    let ref: HTMLInputElement;

    onMount(() => autoFocus && (ref?.focus() !== undefined))
</script>

<div class="flex flex-col gap-2">
    <Text>{title}</Text>
    {#each options as [value, label]}
        <div class="flex gap-2 px-4">
            <input id={value} type="radio" value={value} name={name} required={required}/>
            <label for={value}>{label}</label>
        </div>
    {/each}
</div>

{#if error}
    <div class="label label-text text-error mt-1">{error}</div>
{/if}




