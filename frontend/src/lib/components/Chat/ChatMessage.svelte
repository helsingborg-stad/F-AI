<script lang="ts">
  import dayjs from 'dayjs'
  import MarkdownIt from 'markdown-it'
  import DOMPurify from 'isomorphic-dompurify'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    sender?: string
    details?: string
    text?: string
    time?: string
    showLoader: boolean
  }

  const {
    sender,
    details = '',
    text = '',
    time = '',
    showLoader,
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
      <div class="prose prose-sm max-w-none">
        {#if details}
          <details class="group w-full mb-2">
            <summary class="cursor-pointer list-none bg-gray-100 hover:bg-gray-200 p-2 rounded-t">
              <span class="group-open:rotate-90 inline-block transition-transform">▶</span>
              <span class="ml-2">Show reasoning</span>
            </summary>
            <div class="p-2 border rounded-b">
              <span>{details}</span>
            </div>
          </details>
        {/if}

        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html renderedMarkdown}
        {#if showLoader}
          <Icon icon={icons.loading} />
        {/if}
      </div>
    </div>
  </div>
</div>
