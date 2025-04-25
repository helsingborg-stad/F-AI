<script lang="ts">
  interface Props {
    height?: string;
  }

  const {
    height = 'full',
  }: Props = $props()
</script>

<div class={`mx-4 h-${height} border-l border-gray-200`}></div>
