<script lang="ts">
  import InlineSvgIcon from './SVG.svelte'
  import Badge from './Badge.svelte'
  import { path, searchParams } from 'elegua'
  import { matchCurrentPath } from '../../util/match-path'

  let className = ''
  export { className as class }
  export let text: string | null = null
  export let href: string | null = null
  export let active: boolean | string = false
  export let disabled: boolean = false

  export let underline: 'always' | 'never' | 'on-hover' | boolean = false

  export let state:
    | 'primary'
    | 'secondary'
    | 'accent'
    | 'success'
    | 'info'
    | 'warning'
    | 'error'
    | null = null

  export let badge: string | number | null = null
  export let badgeState:
    | 'primary'
    | 'secondary'
    | 'accent'
    | 'success'
    | 'info'
    | 'warning'
    | 'error'
    | null = null

  export let iconSrc: string | null = null
  export let iconState:
    | 'primary'
    | 'secondary'
    | 'accent'
    | 'success'
    | 'info'
    | 'warning'
    | 'error'
    | null = null

  $: stateClass = state ? `link-${state}` : null

  const {} = $$props
</script>

<a
  {href}
  class:link={['always', true, 'on-hover'].includes(underline)}
  class:link-hover={underline === 'on-hover'}
  class:link-active={active === true ||
    (typeof active === 'string' && matchCurrentPath(active, $path, $searchParams))}
  class:active={active === true ||
    (typeof active === 'string' && matchCurrentPath(active, $path, $searchParams))}
  class:link-disabled={disabled}
  class:link-primary={state === 'primary'}
  class:link-secondary={state === 'secondary'}
  class:link-accent={state === 'accent'}
  class:link-success={state === 'success'}
  class:link-info={state === 'info'}
  class:link-warning={state === 'warning'}
  class:link-error={state === 'error'}
  class={className ?? null}
>
  {#if iconSrc}
    <InlineSvgIcon state={iconState} src={iconSrc} />
  {/if}

  <slot>{text}</slot>

  {#if badge}
    <Badge state={badgeState}>{badge}</Badge>
  {/if}
</a>
