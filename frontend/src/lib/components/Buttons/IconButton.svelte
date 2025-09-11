<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    icon: string
    onClick: () => void
    tooltip?: string
    disabled?: boolean
  }

  const { icon, onClick, tooltip, disabled }: Props = $props()
</script>

<div class="tooltip" data-tip={tooltip}>
  <button class="btn btn-sm" class:btn-disabled={disabled} {disabled} onclick={onClick}>
    <Icon {icon} width={16} height={16} />
  </button>
</div>
