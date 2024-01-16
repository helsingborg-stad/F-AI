<script lang="ts">
    import {writable} from 'svelte/store';
    import RenderDynamicComponents from "./RenderDynamicComponents.svelte";

    export let path: string;

    const data = writable(null);
    const error = writable(null);


    async function fetchData() {
        error.set(null);
        try {
            const response = await fetch(`/api${path}`);
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            const json = await response.json();
            data.set(json);
        } catch (e: any) {
            error.set(e.message);
        }
    }


    $: path && fetchData() && console.log(path) == null && console.log(data) == null
</script>

<!-- Display the fetched data or an error message -->
<div>
    {#if $error}
        <p style="color: red">Error: {$error}</p>
    {:else if $data}
        <RenderDynamicComponents components={$data}/>
        <!--        <pre>{JSON.stringify($data, null, 2)}</pre>-->
    {:else}
        <p>Loading...</p>
    {/if}
</div>
