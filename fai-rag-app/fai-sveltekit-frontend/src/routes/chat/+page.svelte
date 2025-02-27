<script lang="ts">
  import { writable } from 'svelte/store'
  import ChatBubble from '$lib/components/Chat/ChatBubble.svelte'
  import type { MessageType } from '$lib/types.js'
  import ChatInput from '$lib/components/Chat/ChatInput.svelte'

  let messages = writable<MessageType[]>([])

  const sendMessage = async (message: string) => {
    if (message.trim() === '') return

    messages.update((msgs) => [...msgs, { sender: 'user', text: message }])

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      })

      const data = await response.json()

      if (response.ok) {
        // Add the back-end's response to the chat
        messages.update((msgs) => [...msgs, { sender: 'bot', text: data.response }])
      } else {
        console.error('Error:', data.error)
        messages.update((msgs) => [
          ...msgs,
          { sender: 'bot', text: 'An error occurred. Please try again.' },
        ])
      }
    } catch (error) {
      console.error('Error:', error)
      messages.update((msgs) => [
        ...msgs,
        { sender: 'bot', text: 'An error occurred. Please try again.' },
      ])
    }

    // Clear the input field
    message = ''
  }
</script>

<!-- Chat Content -->
<div class="flex h-full flex-1 flex-col bg-gradient-to-b from-orange-50 to-orange-100">
  <!-- Chat Bubbles Area -->
  <div class="flex-1 overflow-y-auto p-4">
    {#each $messages as msg (msg.text)}
      <ChatBubble sender={msg.sender} text={msg.text} />
    {/each}
  </div>

  <!-- Chat Input -->
  <div class="p-2">
    <div class="m-3.5 rounded-2xl bg-white p-2">
      <ChatInput send={sendMessage} placeholder="Fråga Folkets AI" />
    </div>
  </div>
</div>
