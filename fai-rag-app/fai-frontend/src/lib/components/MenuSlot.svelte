<script lang="ts">

    import type {IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = []
</script>


{#each components as component}
    <li>
        <slot>
            <slot name="links" component={component}/>
        </slot>
    </li>
{/each}
