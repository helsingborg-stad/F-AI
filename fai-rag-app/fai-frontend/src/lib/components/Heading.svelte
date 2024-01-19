<!-- Heading.svelte -->
<script lang="ts">
    import InlineSvgIcon from "./SVG.svelte";
    import Badge from "./Badge.svelte";

    export let level: number = 1; // Default to h1
    export let text: string = '';

    let className: string | undefined

    export {className as class}

    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    export let badge: string | number | null = null
    export let badgeState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    export let iconSrc: string | null = null
    export let iconState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | 'neutral' | null = null

    // Determine the heading type dynamically based on the level prop
    $: Tag = `h${Math.min(6, Math.max(1, level))}` as keyof HTMLElementTagNameMap;
</script>

<svelte:element this={Tag} class={[className, state ?? null].join(' ')}>
    {#if iconSrc}
        <InlineSvgIcon src={iconSrc} state={iconState}/>
    {/if}

    <slot>{text}</slot>

    {#if badge}
        <Badge state={badgeState}>{badge}</Badge>
    {/if}

</svelte:element>
