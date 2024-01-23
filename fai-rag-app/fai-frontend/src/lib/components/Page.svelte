<script lang="ts">
    import type {IRenderableComponent} from "../types"
    import Container from "./Container.svelte"

    export let components: IRenderableComponent[] = []
</script>

<div>
    <Container>
        <slot>
            {#each components as component}
                <svelte:component this={component.type} {...component.props}/>
            {/each}
        </slot>
    </Container>
</div>