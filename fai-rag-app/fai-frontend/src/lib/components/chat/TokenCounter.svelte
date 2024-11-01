<script lang="ts">
  export let maxTokens = -1
  export let exceededTokenCount = false

  export function queueUpdateTokenCount(text: string, conversationId: string | null, assistantId: string | null) {
    clearTimeout(tokenTimeoutHandle)
    tokenTimeoutHandle = setTimeout(() => updateTokenCount(text, conversationId, assistantId), 1000)
  }

  let tokenCount = -1
  let tokenTimeoutHandle = -1

  $: exceededTokenCount = maxTokens > 0 && tokenCount > maxTokens

  function updateTokenCount(text: string, conversationId: string | null, assistantId: string | null) {
    console.log(text, conversationId, assistantId)
    fetch(`/api/count-tokens`, {
        method: 'POST',
        body: JSON.stringify({ text, conversation_id: conversationId, assistant_id: assistantId }),
        headers: {
          'Content-Type': 'application/json',
        },
      },
    ).then(res => res.json())
      .then(res => {
        tokenCount = res?.count ?? -1
      })
      .catch(() => {
        tokenCount = -1
      })
      .finally(() => {
        tokenTimeoutHandle = -1
      })
  }
</script>

<span
  class:hidden={maxTokens <= 0}
  class="block text-right text-xs"
>
  {#if tokenTimeoutHandle >= 0}
    ...
  {:else if tokenCount >= 0}
    {tokenCount}/{maxTokens}
  {:else}
    ?
  {/if}
</span>