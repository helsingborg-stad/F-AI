<script lang="ts">
  export let placeholder: string = '';
  export let send: (message: string) => void = () => {};

  let message = '';

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault();
      const currentMessage = (e.target as HTMLInputElement).value;
      handleSend(currentMessage);
    }
  }

  function handleSend(currentMessage: string) {
    if (currentMessage.trim() === '') return;
    send(currentMessage);
    message = '';
  }
</script>

<div class="flex items-center gap-2">
  <button
    class="btn btn-ghost btn-circle text-gray-800"
    on:click={() => console.log('Attach file')}
    aria-label="Send message"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-paperclip"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
  </button>
  <input
    type="text"
    class="flex-grow border-0 bg-white rounded-full px-4 py-2 text-gray-800 placeholder-gray-400"
    placeholder={placeholder}
    bind:value={message}
    on:keydown={handleKeyDown}
  />
  <button
    class="btn btn-square bg-orange-600 text-gray-50"
    on:click={() => handleSend(message)}
    aria-label="Send message"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
  </button>
</div>

