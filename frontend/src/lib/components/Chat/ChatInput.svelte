<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import ActionButtons, {
    type AllowedFeature,
  } from '$lib/components/Chat/ChatInput/ActionButtons.svelte'
  import AttachedFile from '$lib/components/AttachedFile/AttachedFile.svelte'
  import type { IAssistantMenu } from '$lib/types.js'
  import type { FileWithState } from '$lib/files/useInlineFiles.js'

  interface Props {
    placeholder: string
    value: string
    onSubmit: () => void
    disabled: boolean
    receivingMessage: boolean
    onStopChat: () => void
    selectedAssistantId: string
    assistants: IAssistantMenu[]
    disableAssistantPicker: boolean
    allowedFeatures: AllowedFeature[]
    enabledFeatures: string[]
    onFilesChanged: (files: File[]) => void
    inlineFiles: FileWithState[]
    canChangeFiles: boolean
  }

  let {
    placeholder,
    value = $bindable(),
    onSubmit,
    disabled,
    receivingMessage,
    onStopChat,
    selectedAssistantId = $bindable(),
    assistants,
    disableAssistantPicker,
    allowedFeatures,
    enabledFeatures = $bindable(),
    onFilesChanged,
    inlineFiles,
    canChangeFiles,
  }: Props = $props()

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

  function removeFile(fileId: string) {
    const newFiles = inlineFiles.filter((f) => f.id !== fileId).map((f) => f.file)
    onFilesChanged(newFiles)
  }
</script>

<div class="flex flex-col gap-2 rounded-2xl p-3">
  <div>
    <textarea
      bind:this={textareaElement}
      rows="1"
      bind:value
      {placeholder}
      class="textarea max-h-40 min-h-[20px] w-full resize-none overflow-y-hidden border-none px-1 focus:outline-none"
      {disabled}
      oninput={autoResize}
      onkeydown={handleTextareaKeyDown}
    ></textarea>
  </div>
  <div
    role="toolbar"
    tabindex="0"
    onclick={handleDivClick}
    onkeydown={handleKeyDown}
    class="flex flex-col gap-2"
  >
    <div class="flex max-w-full flex-row gap-2 overflow-x-scroll">
      {#each inlineFiles as file (file.file.name)}
        <AttachedFile
          title={file.id}
          state={file.state}
          onRemove={() => removeFile(file.id)}
        />
      {/each}
    </div>
    <div class="flex items-center">
      <div class="grow">
        <ActionButtons
          {allowedFeatures}
          bind:enabledFeatureIds={enabledFeatures}
          {assistants}
          bind:selectedAssistantId
          {disableAssistantPicker}
          {onFilesChanged}
          {canChangeFiles}
        />
      </div>
      {#if !receivingMessage}
        <div
          class={disableSend ? 'tooltip' : ''}
          data-tip={value === ''
            ? m.chat_input_tooltip_empty_message()
            : m.chat_input_tooltip_select_assistant()}
        >
          <button class="btn btn-sm" onclick={handleSend} disabled={disableSend}>
            {m.chat_input_action_send()}
          </button>
        </div>
      {:else}
        <button class="btn btn-sm" onclick={onStopChat}>
          {m.chat_input_action_abort()}
        </button>
      {/if}
    </div>
  </div>
</div>
