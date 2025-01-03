<script lang="ts">
  export let sender: 'user' | 'bot' = 'bot';
  export let text: string = '';
  export let name: string = '';
  export let time: string = '';
  export let avatar: string = '';
  export let status: string = '';
  export let bubbleColor: string = ''; // e.g., 'primary', 'secondary', 'accent', etc.

  $: alignmentClass = sender === 'user' ? 'chat-end' : 'chat-start';

  $: bubbleClass = bubbleColor ? `chat-bubble-${bubbleColor}` : '';
</script>

<div class="chat {alignmentClass}">
  {#if avatar}
    <div class="chat-image avatar">
      <div class="w-10 rounded-full">
        <img src="{avatar}" alt="{name}" />
      </div>
    </div>
  {/if}
  {#if name || time}
    <div class="chat-header">
      {#if name}{name}{/if}
      {#if time}
        <time class="text-xs opacity-50 ml-2">{time}</time>
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
