<script lang="ts">
  import type { Snippet } from 'svelte'

  interface Props {
    placeholder: string
    value: string
    onSubmit: () => void
    children: Snippet
    disabled: boolean
    receivingMessage: boolean
    onStopChat: () => void
  }

  let { placeholder, value = $bindable(), onSubmit, children, disabled, receivingMessage, onStopChat }: Props = $props()

  let disableSend = $derived.by(() => {
    return disabled || value === ''
  })

  let textareaElement: HTMLTextAreaElement

  function autoResize(e: Event) {
    const target = e.target as HTMLTextAreaElement
    target.style.height = 'auto'
    target.style.height = target.scrollHeight + 'px'

    const maxHeight = parseInt(getComputedStyle(target).maxHeight)
    if (target.scrollHeight >= maxHeight) {
      target.style.overflowY = 'auto'
    } else {
      target.style.overflowY = 'hidden'
    }
  }


  function resetTextareaHeight() {
    if (textareaElement) {
      textareaElement.style.height = 'auto'
    }
  }

  function handleDivClick(e: MouseEvent | TouchEvent) {
    if (receivingMessage) return

    if (e.currentTarget === e.target) {
      textareaElement.focus()
    }
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' || e.key === ' ') {
      textareaElement.focus()
      e.preventDefault()
    }
  }

  function handleTextareaKeyDown(e: KeyboardEvent) {
    if (receivingMessage) return

    if (e.key === 'Enter') {
      if (e.shiftKey) {
        return
      } else {
        e.preventDefault()
        onSubmit()
      }
    }
  }

  function handleSend() {
    onSubmit()
    textareaElement.focus()
  }

  $effect(() => {
    if (value === '') {
      resetTextareaHeight()
    }
  })
</script>

<div class="flex flex-col rounded-2xl p-3 gap-2">
  <div>
      <textarea
        bind:this={textareaElement}
        rows="1"
        bind:value
        {placeholder}
        class="textarea w-full px-1 resize-none focus:outline-none border-none min-h-[20px] max-h-40 overflow-y-hidden"
        disabled={disabled}
        oninput={autoResize}
        onkeydown={handleTextareaKeyDown}
      ></textarea>
  </div>
  <div
    role="toolbar"
    tabindex="0"
    onclick={handleDivClick}
    onkeydown={handleKeyDown}
    class="flex flex-row items-center justify-between"
  >
    <div class="flex-1">
      {@render children()}
    </div>
    <div class="flex-shrink-0">
      {#if !receivingMessage}
        <div class={disableSend ? "tooltip" : ""} data-tip={value === '' ? 'Message is empty' : 'Select assistant'}>
          <button class="btn btn-sm" onclick={handleSend} disabled={disableSend}>Send</button>
        </div>
      {:else }
        <button class="btn btn-sm" onclick={onStopChat}>Abort</button>
      {/if}
    </div>
  </div>
</div>
