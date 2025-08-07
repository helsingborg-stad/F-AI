<script lang="ts">
  interface Props {
    text: string
  }

  const { text }: Props = $props()
</script>

<code class="px-1 font-mono rounded-sm">{text}</code>
