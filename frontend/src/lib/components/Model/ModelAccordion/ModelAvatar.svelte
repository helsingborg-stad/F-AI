<script lang="ts">
  interface Props {
    avatar?: string
    provider: string
    primaryColor: string
    isSelected: boolean
    size?: 'sm' | 'md'
  }

  let { avatar, provider, primaryColor, isSelected, size = 'md' }: Props = $props()
  
  const sizeClasses = {
    sm: 'h-10 w-10',
    md: 'h-12 w-12'
  }
</script>

<div class="avatar flex-shrink-0">
  <div
    class="{sizeClasses[size]} rounded-xl shadow-sm transition-transform duration-200"
    class:scale-105={isSelected}
  >
    {#if avatar}
      <img
        src={avatar}
        alt=""
        class="h-full w-full rounded-xl object-cover"
        role="presentation"
      />
    {:else}
      <div
        class="flex h-full w-full items-center justify-center rounded-xl text-sm font-semibold shadow-inner"
        style="background-color: {primaryColor}"
        role="presentation"
      >
        {provider.substring(0, 2).toUpperCase()}
      </div>
    {/if}
  </div>
</div>
