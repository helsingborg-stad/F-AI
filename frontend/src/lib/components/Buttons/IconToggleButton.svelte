<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    value: boolean
    icon: string
    title: string
  }

  let { value = $bindable(), icon, title }: Props = $props()
</script>

<button
  class="btn btn-sm"
  class:btn-active={value}
  class:text-[#3b82f6]={value}
  class:bg-gray-200={value}
  onclick={() => value = !value}
>
  <Icon icon={icon} width={16} height={16} />
  {title}
</button>
