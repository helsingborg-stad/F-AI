<script lang="ts">
  import ChatBubble from '$lib/components/Chat/ChatBubble.svelte'
  import ChatInput from '$lib/components/Chat/ChatInput.svelte'

  interface Message {
    timestamp: string
    source: string
    message: string
  }

  export interface Props {
    messages: Message[],
    inputPlaceholder: string,
    onSubmitMessage: (message: string) => void
  }

  const { messages, inputPlaceholder, onSubmitMessage }: Props = $props()

  function getBubbleColor(source: string) {
    switch (source) {
      case 'error':
        return 'error'
      case 'user':
        return 'primary'
      default:
        return 'secondary'
    }
  }
</script>

<div class="flex flex-col h-full max-h-full">
  <!-- Chat Bubbles Area -->
  <div class="overflow-auto grow p-4">
    {#each messages as msg (`${msg.timestamp}${msg.message}`)}
      <ChatBubble sender={msg.source} name={msg.source} text={msg.message} time={msg.timestamp}
                  bubbleColor={getBubbleColor(msg.source)} />
    {/each}
  </div>

  <!-- Chat Input -->
  <div class="p-2 ">
    <div class="m-3.5 rounded-2xl border bg-white p-2 bg-orange-400">
      <ChatInput send={onSubmitMessage} placeholder={inputPlaceholder} />
    </div>
  </div>
</div>