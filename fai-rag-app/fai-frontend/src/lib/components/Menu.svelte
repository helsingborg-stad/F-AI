<script lang="ts">
    import MenuSlot from "./MenuSlot.svelte"
    import type {IRenderableComponent} from "../types"
    import AsComponent, {type component} from "./common/AsComponent.svelte"
    import SVG from "./SVG.svelte";

    export let title: string | null = null
    export let subMenu: boolean | null = null
    export let isOpen: boolean | null = null
    export let open: boolean | null = isOpen
    export let variant: 'vertical' | 'horizontal' | null = null
    export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
    export let components: IRenderableComponent[] = []
    let template: component | null = null

    export let iconSrc: string | null = null
    export let iconState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null


    $: {
        isOpen
        open = isOpen
    }
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
    <details {open}>
        <summary>
            {#if iconSrc}
                <SVG
                        state={iconState}
                        src={iconSrc}/>
            {/if}
            <slot name="title">{title}</slot>
        </summary>
        <ul>
            <svelte:component this={template}/>
        </ul>
    </details>
{:else}
    <ul class:menu={!subMenu}
        class:menu-vertical={variant === 'vertical'}
        class:menu-horizontal={variant === 'horizontal'}
        class:menu-xs={size === 'xs'}
        class:menu-sm={size === 'sm'}
        class:menu-md={size === 'md'}
        class:menu-lg={size === 'lg'}
        {...$$restProps}>
        {#if title && !subMenu}
            <li class:menu-title={true}
                class:text-xs={true}>
                <slot name="title">{title}</slot>
            </li>
        {/if}

        <svelte:component this={template}/>
    </ul>
{/if}