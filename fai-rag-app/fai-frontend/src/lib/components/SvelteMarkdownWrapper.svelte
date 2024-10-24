<script lang="ts">
  import SvelteMarkdown from 'svelte-markdown';

  export let source;
  export let options = {};

  const defaultOptions = {
    mangle: false
  }

  const mergedOptions = {
    ...defaultOptions,
    ...options
  }
</script>

<SvelteMarkdown {source} options={mergedOptions}/>
