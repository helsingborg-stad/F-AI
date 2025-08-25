<script lang="ts">
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    iconName: keyof typeof icons
    title: string
    onClick: () => void
  }

  let { iconName, title, onClick }: Props = $props()
</script>

<button
  class="flex cursor-pointer items-center gap-2 rounded-md px-4 py-1.5 text-sm hover:bg-gray-100 active:bg-gray-200"
  onclick={onClick}
>
  {#if iconName && icons[iconName]}
    <Icon icon={icons[iconName]} width={16} height={16} />
  {/if}
  {title}
</button>
