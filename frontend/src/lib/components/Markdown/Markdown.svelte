<script lang="ts">
  import SvelteMarkdown from '@humanspeak/svelte-markdown'
  import Image from './renderers/Image.svelte'
  import Code from './renderers/Code.svelte'
  import CodeSpan from './renderers/CodeSpan.svelte'

  interface Props {
    source: string
  }

  const { source }: Props = $props()
</script>

<SvelteMarkdown
  {source}
  renderers={{
    image: Image,
    code: Code,
    codespan: CodeSpan
  }}
/>
