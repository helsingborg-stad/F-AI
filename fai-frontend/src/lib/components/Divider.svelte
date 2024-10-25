<script lang="ts">
    export let text: string = ''
    export let state:
        'default'   |
        'neutral'   |
        'primary'   |
        'secondary' |
        'accent'    |
        'success'   |
        'info'      |
        'warning'   |
        'error'
        = 'default'
</script>

<div
        class="divider"
        class:divider-neutral={state === 'neutral'}
        class:divider-primary={state === 'primary'}
        class:divider-secondary={state === 'secondary'}
        class:divider-accent={state === 'accent'}
        class:divider-success={state === 'success'}
        class:divider-info={state === 'info'}
        class:divider-warning={state === 'warning'}
        class:divider-error={state === 'error'}
        {...$$restProps}
>
    <slot>{text}</slot>
</div>