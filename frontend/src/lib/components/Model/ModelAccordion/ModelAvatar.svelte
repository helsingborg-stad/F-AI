<script lang="ts">
  interface Props {
    avatar?: string
    provider: string
    primaryColor: string
    isSelected: boolean
  }

  let { avatar, provider, primaryColor, isSelected }: Props = $props()
</script>

<div class="avatar mt-1 flex-shrink-0">
  <div
    class="h-12 w-12 rounded-xl shadow-sm transition-transform duration-200"
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
        class="flex h-full w-full items-center justify-center rounded-xl text-sm font-semibold text-white shadow-inner"
        style="background-color: {primaryColor}"
        role="presentation"
      >
        {provider.substring(0, 2).toUpperCase()}
      </div>
    {/if}
  </div>
</div>
