<script lang="ts">
    import {inlineSvg} from '@svelte-put/inline-svg'

    let className: string | null = null
    export {className as class}
    export let width = '16'
    export let src: string
    export let state: 'primary' | 'secondary' | 'accent' | 'success' | 'info' | 'warning' | 'error' | 'neutral' | null = null
</script>


<svg
        use:inlineSvg={src} {width}
        class:text-primary={state === 'primary'}
        class:text-secondary={state === 'secondary'}
        class:text-accent={state === 'accent'}
        class:text-success={state === 'success'}
        class:text-info={state === 'info'}
        class:text-warning={state === 'warning'}
        class:text-error={state === 'error'}
        class:text-neutral={state === 'neutral'}
        class={className ?? null}
        {...$$restProps}
/>

<style>
    svg.svelte {
        /*filter: drop-shadow(0 0 0.5rem theme('colors.primary'))*/
    }
</style>
