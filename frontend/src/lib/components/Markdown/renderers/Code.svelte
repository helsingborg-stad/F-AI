<script lang="ts">
  import hljs from 'highlight.js'
  import 'highlight.js/styles/tokyo-night-dark.css'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    text: string
    lang: string
  }

  const { text, lang }: Props = $props()
  const html = $derived(hljs.highlight(text, { language: lang || 'plaintext' }).value)

  function copyToClipboard() {
    navigator.clipboard.writeText(text)
  }
</script>

<div class="flex flex-col bg-gray-800 rounded">
  <div class="pl-3 pr-1 pt-1 flex justify-between items-center text-gray-400">
    <span class="">{lang}</span>
    <button class="btn btn-circle btn-ghost btn-sm" onclick={copyToClipboard}>
      <Icon icon={icons['copy']} width={16} height={16} />
    </button>
  </div>
  <pre class="m-0 bg-gray-800"><code class="language-{lang}">{@html html}</code></pre>
</div>
