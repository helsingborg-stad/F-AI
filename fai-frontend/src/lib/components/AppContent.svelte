<script lang="ts">
    import {type IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = [];
</script>

<main
        class:min-h-screen={true}
        class:flex={true}
        class:flex-col={true}
        class:drawer-content={true} {...$$restProps}>
    <slot>
        {#each components as component}
            <svelte:component this={component.type} {...component.props}/>
        {/each}
    </slot>
</main>