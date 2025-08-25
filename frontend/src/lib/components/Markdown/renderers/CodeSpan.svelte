<script lang="ts">
  interface Props {
    text: string
  }

  const { text }: Props = $props()
</script>

<code class="rounded-sm px-1 font-mono">{text}</code>
