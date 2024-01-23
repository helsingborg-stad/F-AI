<script lang="ts">
    import {type IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = [];
</script>

<main
        class:drawer-content={true}
        class:flex={true}
        class:flex-col={true} {...$$restProps}>
    <slot>
        {#each components as component}
            <svelte:component this={component.type} {...component.props}/>
        {/each}
    </slot>
</main>