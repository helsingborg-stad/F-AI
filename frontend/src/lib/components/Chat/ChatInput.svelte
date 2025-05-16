<script lang="ts">
  export let placeholder: string = ''
  export let send: (message: string) => void = () => {
  }

  let message = ''

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault()
      const currentMessage = (e.target as HTMLInputElement).value
      handleSend(currentMessage)
    }
  }

  function handleSend(currentMessage: string) {
    if (currentMessage.trim() === '') return
    send(currentMessage)
    message = ''
  }
</script>

<div class="flex items-center gap-2">
  <input
    type="text"
    class="flex-grow border-0 bg-white rounded-full px-4 py-2 text-gray-800 placeholder-gray-400 focus:outline-none"
    placeholder={placeholder}
    bind:value={message}
    on:keydown={handleKeyDown}
  />
  <button
    class="btn btn-square bg-orange-600 text-gray-50"
    on:click={() => handleSend(message)}
    aria-label="Send message"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up">
      <path d="m5 12 7-7 7 7" />
      <path d="M12 19V5" />
    </svg>
  </button>
</div>
