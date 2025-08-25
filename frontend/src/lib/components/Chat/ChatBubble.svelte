<script lang="ts">
  import dayjs from 'dayjs'

  interface Props {
    sender?: string
    text?: string
    name?: string
    time?: string
    avatar?: string
    status?: string
    bubbleColor?: string // e.g., 'primary', 'secondary', 'accent', etc.
  }

  const {
    sender = '',
    text = '',
    name = '',
    time = '',
    avatar = '',
    status = '',
    bubbleColor = '',
  }: Props = $props()

  const alignmentClass = $derived(sender === 'user' ? 'chat-end' : 'chat-start')
  const bubbleClass = $derived(bubbleColor ? `chat-bubble-${bubbleColor}` : '')

  function parseTimestamp(timestamp: string | undefined) {
    if (!timestamp) return undefined
    const d = dayjs(timestamp)
    if (!d.isValid()) return timestamp
    return d.format('YYYY-MM-DD HH:mm:ss')
  }

  const parsedTime = $derived(parseTimestamp(time))
</script>

<div class="chat {alignmentClass}">
  {#if avatar}
    <div class="avatar chat-image">
      <div class="w-10 rounded-full">
        <img src={avatar} alt={name} />
      </div>
    </div>
  {/if}
  {#if name || parsedTime}
    <div class="chat-header">
      {#if name}{name}{/if}
      {#if parsedTime}
        <time class="ml-2 text-xs opacity-50" datetime={time}>{parsedTime}</time>
      {/if}
    </div>
  {/if}
  <div class="chat-bubble {bubbleClass}">
    {text}
  </div>
  {#if status}
    <div class="chat-footer opacity-50">{status}</div>
  {/if}
</div>
