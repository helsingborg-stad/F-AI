<script lang="ts">
    import InlineSvgIcon from "./SVG.svelte"
    import Badge from "./Badge.svelte"

    export let className: string | null
    export {className as class}
    export let disabled: boolean = false
    export let active: boolean = false
    export let html_type: 'button' | 'submit' | 'reset' = 'button'
    export let variants: 'ghost' | 'outline' | 'link' | 'glass' | null = null
    export let state: 'neutral' | 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
    export let block: boolean | null = null
    export let wide: boolean | null = null
    export let circle: boolean | null = null
    export let square: boolean | null = null
    export let noAnimation: boolean | null = null
    export let onClick: () => any = () => null
    export let label: string | null = null
    export let badge: string | number | null = null
    export let badgeState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let iconSrc: string | null = null
    export let iconState: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
</script>

<button
        class="btn {className}"
        class:btn={true}
        class:btn-block={block}
        class:btn-wide={wide}
        class:btn-circle={circle}
        class:btn-square={square}
        class:no-animation={noAnimation}
        class:btn-xs={size === 'xs'}
        class:btn-sm={size === 'sm'}
        class:btn-md={size === 'md'}
        class:btn-lg={size === 'lg'}
        class:btn-outline={variants === 'outline'}
        class:btn-link={variants === 'link'}
        class:btn-glass={variants === 'glass'}
        class:btn-ghost={variants === 'ghost'}
        class:btn-primary={state === 'primary'}
        class:btn-secondary={state === 'secondary'}
        class:btn-accent={state === 'accent'}
        class:btn-success={state === 'success'}
        class:btn-neutral={state === 'neutral'}
        class:btn-info={state === 'info'}
        class:btn-warning={state === 'warning'}
        class:btn-error={state === 'error'}
        class:btn-active={active}
        class:btn-disabled={disabled}
        disabled={disabled}
        type={html_type}
        on:click={onClick}
>
    {#if iconSrc}
        <InlineSvgIcon
                state={iconState}
                src={iconSrc}/>
    {/if}

    <slot>{label}</slot>

    {#if badge}
        <Badge state={badgeState}>{badge}</Badge>
    {/if}
</button>
