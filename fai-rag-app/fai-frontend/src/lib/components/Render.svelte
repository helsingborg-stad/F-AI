<script lang="ts">
    import type {IComponentDef, IRenderableComponent} from '../types'
    import toRenderable from '../component-factory'
    import {writable} from 'svelte/store'

    export let components: IComponentDef[] | IRenderableComponent[] = []
    let renderables = writable<IRenderableComponent[]>([])

    $: {
        components
        $renderables = components.map(toRenderable)
    }
</script>

{#each $renderables as Component}
    {#if Component?.props?.components && Component?.props?.components?.length > 0}
        <svelte:component this={Component.type} {...Component.props}>
            <svelte:self components={[...Component.props.components]}/>
        </svelte:component>
    {:else }
        <svelte:component this={Component.type} {...Component.props}/>
    {/if}
{/each}