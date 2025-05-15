<script lang="ts">
  import dayjs from 'dayjs'

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
      <p>{text}</p>
    </div>
    {#if parsedTime && sender === 'user'}
      <time class="text-xs opacity-50 absolute -top-5 right-0 whitespace-nowrap" datetime={time}>{parsedTime}</time>
    {/if}
  </div>
</div>
