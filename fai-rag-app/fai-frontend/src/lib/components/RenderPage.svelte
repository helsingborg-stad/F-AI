<script lang="ts">
    import type {IComponentDef, IRenderableComponent} from '../types';
    import toRenderable from '../component-factory';
    import {writable} from 'svelte/store';

    export let components: IComponentDef[] = [];

    let renderables = writable<IRenderableComponent[]>([]);

    const setRenderables = (components: IComponentDef[]) => {
        $renderables = components.map(toRenderable)
    }

    $: components && setRenderables(components)
</script>

{#each $renderables as Component}
    <svelte:component this={Component.type} {...Component.props}/>
{/each}