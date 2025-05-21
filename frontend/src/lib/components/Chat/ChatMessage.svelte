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

  const layoutJustifyCenter = 'flex w-full justify-center'
  const layoutMaxWidth = 'flex w-full px-2 md:w-[50rem]'

  const innerContentClasses = $derived(
    sender === 'user'
      ? `${layoutMaxWidth} justify-end`
      : `${layoutMaxWidth} justify-start`,
  )

  const containerClasses = $derived(
    sender === 'user'
      ? 'bg-gray-200 rounded-lg p-3 max-w-[85%] md:max-w-[30rem]'
      : 'rounded-lg p-3 max-w-[95%] md:max-w-full w-full',
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
  <div class="{layoutJustifyCenter} py-1">
    <div class="{innerContentClasses}">
      <time class="text-xs opacity-50 mr-1" datetime={time}>{parsedTime}</time>
    </div>
  </div>
{/if}

<div class="{layoutJustifyCenter}">
  <div class="{innerContentClasses}">
    <div class="{containerClasses}">
      <!-- eslint-disable-next-line svelte/no-at-html-tags -->
      <div class="prose prose-sm max-w-none">{@html renderedMarkdown}</div>
    </div>
  </div>
</div>