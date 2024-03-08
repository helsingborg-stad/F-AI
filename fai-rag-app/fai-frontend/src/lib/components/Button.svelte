<script lang="ts">
    import InlineSvgIcon from "./SVG.svelte"
    import Badge from "./Badge.svelte"
    import {createEventDispatcher} from 'svelte';

    const dispatch = createEventDispatcher();
    export let onClick = () => {
        dispatch('click')
    }
    export let className: string | null
    export {className as class}
    export let disabled: boolean = false
    export let active: boolean = false
    export let html_type: 'button' | 'submit' | 'reset' = 'button'
    export let variant: 'ghost' | 'outline' | 'link' | 'glass' | null = null
    export let state: 'neutral' | 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
    export let block: boolean | null = null
    export let wide: boolean | null = null
    export let circle: boolean | null = null
    export let square: boolean | null = null
    export let noAnimation: boolean | null = null
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
        class:btn-outline={variant === 'outline'}
        class:btn-link={variant === 'link'}
        class:btn-glass={variant === 'glass'}
        class:btn-ghost={variant === 'ghost'}
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
    {#if html_type === 'submit'}
        <span class="loading loading-spinner hidden group-[.is-submitting]:block"></span>
    {/if}
    {#if iconSrc}
        <InlineSvgIcon
                width="24"
                state={iconState}
                src={iconSrc}/>
    {/if}

    <slot>{label ?? ''}</slot>

    {#if badge}
        <Badge state={badgeState}>{badge}</Badge>
    {/if}
</button>
