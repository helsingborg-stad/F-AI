<script lang="ts" context="module">
    import type {IComponentDef} from "./lib/types";

    async function fetchRouteData(path: string, searchParams: URLSearchParams): Promise<IComponentDef[]> {
        const response = await fetch(`/api${path + (searchParams?.toString() ? '?' + searchParams.toString() : '')}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        return await response.json();
    }
</script>

<script lang="ts">
    import {path, searchParams, url} from 'elegua';
    import {writable} from "svelte/store";
    import Render from "./lib/components/Render.svelte";

    import {pageDataStore} from "./lib/store";

    const error = writable<any>(null)

    $: {
        $url
        error.set(null)
        fetchRouteData($path, $searchParams)
            .then((responseData: IComponentDef[]) => $pageDataStore = responseData)
            .catch((e) => error.set(e.message))
    }
</script>


{#if $error}
    <div class="h-screen flex flex-col items-center justify-center">
        <p class="text-center text-xl text-error">{$error}</p>
    </div>
{:else if $pageDataStore}
    <Render bind:components={$pageDataStore}/>
{:else}
    <div class="h-screen flex flex-col items-center justify-center">
        <p class="text-center text-xl text-info">Loading...</p>
    </div>
{/if}

