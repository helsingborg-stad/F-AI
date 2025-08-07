<script lang="ts">
  import SvelteMarkdown from '@humanspeak/svelte-markdown'
  import Image from './renderers/Image.svelte'

  interface Props {
    source: string
  }

  const { source }: Props = $props()
</script>

<SvelteMarkdown
  {source}
  renderers={{
    image: Image,
  }}
/>
