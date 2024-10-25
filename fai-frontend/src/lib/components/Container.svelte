<script lang="ts">
    import type {IRenderableComponent} from "../types"

    export let className: string = '';
    export let components: IRenderableComponent[] = [];
</script>

<div class={['container', 'mx-auto', 'px-6',className].join(' ')}>
    <slot>
        {#each components as component}
            <svelte:component this={component.type} {...component.props}/>
        {/each}
    </slot>
</div>
