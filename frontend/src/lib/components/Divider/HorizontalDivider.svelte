<script lang="ts">
  interface Props {
    height?: string
    marginY?: string
    bgColor?: string
    borderWidth?: string
  }

  const {
    height = 'px',
    marginY = '1',
    bgColor = 'gray-200',
    borderWidth = '1',
  }: Props = $props()

  const dividerClass = `h-${height} my-${marginY} bg-${bgColor} border-${borderWidth}`
</script>

<hr class={dividerClass} />
