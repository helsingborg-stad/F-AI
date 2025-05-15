<script lang="ts">
  import dayjs from 'dayjs'
  import MarkdownIt from 'markdown-it'
  import DOMPurify from 'isomorphic-dompurify'

  interface Props {
    sender?: string
    text?: string
    time?: string
  }

  const {
    sender,
    text = '',
    time = '',
  }: Props = $props()

  const md = new MarkdownIt({
    html: false,        // Disable HTML tags in source
    breaks: true,       // Convert '\n' in paragraphs into <br>
    linkify: true,      // Autoconvert URL-like text to links
    typographer: true,  // Enable smartquotes and other typographic replacements
  })

  const renderedMarkdown = $derived(DOMPurify.sanitize(md.render(text)))

  const messageClasses = $derived(
    sender === 'user'
      ? 'flex justify-end'
      : 'flex justify-center',
  )

  const containerClasses = $derived(
    sender === 'user'
      ? 'bg-gray-200 rounded-lg p-3'
      : 'rounded-lg p-3 w-[40rem]',
  )

  function parseTimestamp(timestamp: string | undefined) {
    if (!timestamp) return undefined
    const d = dayjs(timestamp)
    if (!d.isValid()) return timestamp
    return d.format('YYYY-MM-DD HH:mm:ss')
  }

  const parsedTime = $derived(parseTimestamp(time))
</script>

{#if sender === 'user'}
  <div class="{messageClasses} py-1 pr-1">
    <time class="text-xs opacity-50 ml-2" datetime={time}>{parsedTime}</time>
  </div>
{/if}

<div class="{messageClasses}">
  <div>
    <div class="{containerClasses}">
      <!-- eslint-disable-next-line svelte/no-at-html-tags -->
      <div class="prose prose-sm max-w-none">{@html renderedMarkdown}</div>
    </div>
  </div>
</div>


