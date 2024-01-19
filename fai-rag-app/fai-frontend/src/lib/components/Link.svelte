<script lang="ts">
    import InlineSvgIcon from "./SVG.svelte";
    import Badge from "./Badge.svelte";

    export let title: string | null = null
    export let href: string = ''
    export let active: boolean = false
    export let disabled: boolean = false

    export let underline: 'always' | 'never' | 'on-hover' | boolean = false

    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    export let badge: string | number | null = null
    export let badgeState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    export let iconSrc: string | null = null
    export let iconState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null

    $: stateClass = state ? `link-${state}` : null

    const {} = $$props

</script>

<a {href} class:link={['always', true, 'on-hover'].includes(underline)}
   class:link-hover={underline === 'on-hover'} class={stateClass}
>
    {#if iconSrc}
        <InlineSvgIcon
                state={iconState}
                src={iconSrc}/>
    {/if}

    <slot>{title}</slot>

    {#if badge}
        <Badge state={badgeState}>{badge}</Badge>
    {/if}

</a>