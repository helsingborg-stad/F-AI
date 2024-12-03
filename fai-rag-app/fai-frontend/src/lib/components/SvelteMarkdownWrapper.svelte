<script lang="ts">
  import SvelteMarkdown from 'svelte-markdown'
  import Link from '$lib/components/markdown/Link.svelte'

  export let source: string
  export let options = {}

  const defaultOptions = {
    mangle: false,
  }

  const mergedOptions = {
    ...defaultOptions,
    ...options,
  }
</script>

<SvelteMarkdown {source} options={mergedOptions} renderers={{ link: Link }} />
