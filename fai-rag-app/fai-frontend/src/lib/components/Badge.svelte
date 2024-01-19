<script lang="ts">

    export let text: string | null = null;
    export let className: string | null;
    export {className as class};
    export let variants: 'ghost' | 'outline' | null = null
    export let state: 'neutral' | 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | null = null
    export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
</script>

<div
        class:badge={true}
        class:badge-xs={size === 'xs'}
        class:badge-sm={size === 'sm'}
        class:badge-md={size === 'md'}
        class:badge-lg={size === 'lg'}
        class:badge-outline={variants === 'outline'}
        class:badge-ghost={variants === 'ghost'}
        class:badge-primary={state === 'primary'}
        class:badge-netural={state === 'neutral'}
        class:badge-secondary={state === 'secondary'}
        class:badge-accent={state === 'accent'}
        class:badge-success={state === 'success'}
        class:badge-info={state === 'info'}
        class:badge-warning={state === 'warning'}
        class:badge-error={state === 'error'}
        class="{className}"
        {...$$restProps}
>
    <slot name="before"/>
    <slot>{text}</slot>
    <slot name="after"/>
</div>
