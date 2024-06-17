<script lang="ts">

    import type {IRenderableComponent} from "../types"

    export let components: IRenderableComponent[] = []

    let className = ''
    export {className as class}
</script>


{#each components as component}
    <li class:disabled={component?.props?.disabled === true} class={className}>
        <slot>
            <slot name="links" component={component}/>
        </slot>
    </li>
{/each}
