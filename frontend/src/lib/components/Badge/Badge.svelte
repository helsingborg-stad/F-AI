<script lang="ts">
  import Image from 'lucide-svelte/icons/image'
  import Star from 'lucide-svelte/icons/star'
  import Code from 'lucide-svelte/icons/code'
  import LayoutDashboard from 'lucide-svelte/icons/layout-dashboard'
  import Search from 'lucide-svelte/icons/search'

  type BadgeType = 'image' | 'reasoning' | 'function-calling' | 'web-search' | 'tokens' | 'provider'
  type BadgeSize = 'xs' | 'sm' | 'md' | 'lg'
  type BadgeVariant = 'filled' | 'outline'

  interface Props {
    type?: BadgeType
    size?: BadgeSize
    variant?: BadgeVariant
    label?: string
    value?: string | number
    isSelected?: boolean
  }

  let {
    type = $bindable(),
    size = 'xs',
    variant = 'filled',
    label = $bindable(),
    value = $bindable(),
    isSelected = false,
  }: Props = $props()

  const badgeConfig: Record<
    BadgeType,
    {
      color: string
      icon: typeof Image | null
      defaultLabel: string
    }
  > = {
    image: {
      color: 'badge-info',
      icon: Image,
      defaultLabel: 'Images',
    },
    reasoning: {
      color: 'badge-success',
      icon: Star,
      defaultLabel: 'Reasoning',
    },
    'function-calling': {
      color: 'badge-accent',
      icon: Code,
      defaultLabel: 'Function Calling',
    },
    'web-search': {
      color: 'badge-info',
      icon: Search,
      defaultLabel: 'Web Search',
    },
    tokens: {
      color: 'badge-warning',
      icon: LayoutDashboard,
      defaultLabel: 'tokens',
    },
    provider: {
      color: 'badge-neutral',
      icon: null,
      defaultLabel: '',
    },
  }

  const config = $derived(type ? badgeConfig[type] : null)

  const badgeColor = $derived.by(() => {
    if (type === 'provider' && isSelected) {
      return 'badge-primary'
    }
    return config?.color || 'badge-neutral'
  })

  const displayLabel = $derived(label || config?.defaultLabel || '')

  const displayValue = $derived.by(() => {
    if (!value) return ''
    if (type === 'tokens' && typeof value === 'number') {
      return value.toLocaleString()
    }
    return String(value)
  })

  const badgeClasses = $derived.by(() => {
    const classes = [
      'badge',
      `badge-${size}`,
      badgeColor,
      variant === 'outline' ? 'badge-outline' : '',
      config?.icon || displayValue ? 'gap-1' : '',
      config?.icon && size === 'xs' ? 'py-0.5' : '',
    ]
    return classes.filter(Boolean).join(' ')
  })

  const iconSize = $derived.by(() => {
    switch (size) {
      case 'xs':
        return 12
      case 'sm':
        return 14
      case 'md':
        return 16
      case 'lg':
        return 18
      default:
        return 12
    }
  })

  const IconComponent = $derived(config?.icon)
</script>

<span class={badgeClasses}>
  {#if IconComponent}
    <IconComponent size={iconSize} />
  {/if}
  {#if displayLabel}
    {displayLabel}
  {/if}
  {#if displayValue && displayLabel}
    {' '}
  {/if}
  {#if displayValue}
    {displayValue}
  {/if}
</span>
