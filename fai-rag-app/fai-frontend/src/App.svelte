<script lang="ts">
    import {path, resolve, params, match, goto} from 'elegua';
    import FetchAPIComponent from './lib/components/FetchAPIComponent.svelte';
</script>

<FetchAPIComponent path={$path}/>