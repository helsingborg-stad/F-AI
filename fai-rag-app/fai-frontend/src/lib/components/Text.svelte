<!-- Heading.svelte -->
<script lang="ts">
    import InlineSvgIcon from "./SVG.svelte"
    import Badge from "./Badge.svelte"

    export let text: string = ''
    export let element: keyof HTMLElementTagNameMap = 'span'
    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    let className: string | null = null
    export {className as class}

    export let badge: string | number | null = null
    export let badgeState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let iconSrc: string | null = null
    export let iconState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | 'neutral' | null = null

</script>

<svelte:element
        this={element}
        class={className}
        {...$$restProps}
>
    <slot {...$$props} name="before"/>

    {#if iconSrc}
        <InlineSvgIcon src={iconSrc} state={iconState}/>
    {/if}

    <slot {...$$props}>{text}</slot>

    {#if badge}
        <Badge state={badgeState}>{badge}</Badge>
    {/if}

    <slot {...$$props} name="after"/>
</svelte:element>
