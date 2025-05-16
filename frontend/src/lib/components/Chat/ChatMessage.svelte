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

  const messageClasses = 'flex justify-center'

  const innerContentClasses = $derived(
    sender === 'user'
      ? 'flex justify-end w-[50rem]'
      : 'flex justify-center w-[50rem]'
  )

  const containerClasses = $derived(
    sender === 'user'
      ? 'bg-gray-200 rounded-lg p-3 max-w-[30rem]'
      : 'rounded-lg p-3 w-[50rem]',
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
  <div class="flex justify-center py-1 pr-1">
    <div class="w-[50rem] flex justify-end">
      <time class="text-xs opacity-50 ml-2" datetime={time}>{parsedTime}</time>
    </div>
  </div>
{/if}

<div class="{messageClasses}">
  <div class="{innerContentClasses}">
    <div class="{containerClasses}">
      <!-- eslint-disable-next-line svelte/no-at-html-tags -->
      <div class="prose prose-sm max-w-none">{@html renderedMarkdown}</div>
    </div>
  </div>
</div>