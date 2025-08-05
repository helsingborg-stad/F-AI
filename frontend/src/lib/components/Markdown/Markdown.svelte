<script lang="ts">
  import SvelteMarkdown from '@humanspeak/svelte-markdown'

  interface Props {
    source: string
  }

  const { source }: Props = $props()
</script>

<SvelteMarkdown {source} />
