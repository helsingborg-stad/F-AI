<script lang="ts">

    import MenuSlot from "./MenuSlot.svelte";
    import type {IRenderableComponent} from "../types";
    import AsComponent, {type component} from "./common/AsComponent.svelte";

    let className = '';
    export {className as class}
    export let title: string | null = null;
    export let subMenu: boolean | null = null;
    export let isOpen: boolean | null = null;
    export let variant: 'vertical' | 'horizontal' | null = null
    export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
    export let components: IRenderableComponent[] = [];

    let template: component | null = null;
</script>


<AsComponent bind:component={template}>
    {#if !components || components.length === 0}
        <slot/>
    {:else}
        <MenuSlot {components}>
            <svelte:fragment slot="links" let:component={{type, props}}>
                <svelte:component this={type} {...props}/>
            </svelte:fragment>
        </MenuSlot>
    {/if}
</AsComponent>

{#if subMenu}
    <details open={isOpen}>
        <summary>
            <slot name="title">{title}</slot>
        </summary>
        <ul>
            <svelte:component this={template}/>
        </ul>
    </details>
{:else}
    <ul class={`menu text-sm menu-${variant} ${className}`}
        class:menu-xs={size === 'xs'}
        class:menu-sm={size === 'sm'}
        class:menu-md={size === 'md'}
        class:menu-lg={size === 'lg'}
    >
        {#if title && !subMenu}
            <li class="menu-title  text-sm">
                <slot name="title">{title}</slot>
            </li>
        {/if}

        <svelte:component this={template}/>
    </ul>
{/if}

