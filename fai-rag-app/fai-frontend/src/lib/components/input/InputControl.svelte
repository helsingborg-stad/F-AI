<script lang="ts">
  import { Label } from '$lib/components/input/index'

  export let name: string
  export let error: string | null = null
  export let label: string | null = null
  export let size: 'xs' | 'sm' | 'md' | 'lg' | null = null
</script>

<label
  class:form-control={1}
  class:text-xs={size === 'xs'}
  class:text-sm={size === 'xs'}
  class:text-md={size === 'sm'}
  class:text-lg={size === 'md'}
  for={name}
  {...$$restProps}
>
  <slot name="label" label>
    {#if label !== null}
      <Label>{label}</Label>
    {/if}
  </slot>
  <slot />
  <slot name="helper" {error}>
    {#if error !== null}
      <Label altText={error} />
    {/if}
  </slot>
</label>
