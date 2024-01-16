<script lang="ts">
    import type {IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = [];

    let className: string | undefined

    export {className as class}

    const props = {
        ...className ? {class: className} : {}
    }
</script>

<div {...props}>
    <slot>
        {#each components as component}
            <svelte:component this={component.type} {...component.props}/>
        {/each}
    </slot>
</div>
