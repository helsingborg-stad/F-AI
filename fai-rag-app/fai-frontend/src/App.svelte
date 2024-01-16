<script lang="ts">
    import {path, searchParams} from 'elegua';
    import {pageDataStore} from "./lib/store/page";
    import RenderDynamicComponents from "./lib/components/RenderDynamicComponents.svelte";
    import {writable} from "svelte/store";

    const error = writable<any>(null)

    async function fetchData() {
        error.set(null);
        try {
            const response = await fetch(`/api${$path + ($searchParams?.toString() ? '?' + $searchParams.toString() : '')}`);
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            const json = await response.json();
            pageDataStore.set(json);
        } catch (e: any) {
            error.set(e.message);
        }
    }

    $: {
        $path
        $searchParams
        fetchData()
    }


    $: {
        $pageDataStore
    }

</script>


{#if $error}
    <div class="h-screen flex flex-col items-center justify-center">
        <p class="text-center text-xl text-error">{$error}</p>
    </div>
{:else if $pageDataStore}
    <RenderDynamicComponents bind:components={$pageDataStore}/>
{:else}
    <div class="h-screen flex flex-col items-center justify-center">
        <p class="text-center text-xl text-info">Loading...</p>
    </div>
{/if}
