<script lang="ts">
  import dayjs from 'dayjs'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import Markdown from '$lib/components/Markdown/Markdown.svelte'

  interface Props {
    sender?: string
    details?: string
    text?: string
    time?: string
    showLoader: boolean
  }

  const { sender, details = '', text = '', time = '', showLoader }: Props = $props()

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
    <div class={innerContentClasses}>
      <time class="mr-1 text-xs opacity-50" datetime={time}>{parsedTime}</time>
    </div>
  </div>
{/if}

<div class={layoutJustifyCenter}>
  <div class={innerContentClasses}>
    <div class={containerClasses}>
      <div class="prose prose-sm max-w-none">
        {#if details}
          <details class="group mb-2 w-full">
            <summary
              class="cursor-pointer list-none rounded-t bg-gray-100 p-2 hover:bg-gray-200"
            >
              <span class="inline-block transition-transform group-open:rotate-90"
                >▶</span
              >
              <span class="ml-2">Show reasoning</span>
            </summary>
            <div class="rounded-b border p-2">
              <span>{details}</span>
            </div>
          </details>
        {/if}

        <Markdown source={text} />
        {#if showLoader}
          <Icon icon={icons.loading} />
        {/if}
      </div>
    </div>
  </div>
</div>
