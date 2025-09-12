<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import ColorPicker from '$lib/components/ColorPicker/ColorPicker.svelte'
  import { MODEL_COLORS } from '$lib/constants/colors.js'

  interface Props {
    avatarBase64: string
    altImagePlaceholder: string
    primaryColor: string
  }

  let { avatarBase64, altImagePlaceholder, primaryColor }: Props = $props()

  const colors = MODEL_COLORS

  let selectedColor = $state(
    primaryColor && primaryColor !== '#ffffff'
      ? primaryColor
      : colors[Math.floor(Math.random() * (colors.length - 1)) + 1],
  )
  let enableImagePlaceholder = $state(!avatarBase64)
  let imagePreviewUrl = $state(
    avatarBase64 ? `data:image/png;base64,${avatarBase64}` : '',
  )
  let deleteAvatar = $state(false)
  let fileInput: HTMLInputElement
  let currentAvatarBase64 = $state(avatarBase64)

  function handleColorSelect(color: string) {
    selectedColor = color
  }

  function handleFileChange(event: Event) {
    const fileInput = event.target as HTMLInputElement

    if (fileInput.files && fileInput.files[0]) {
      imagePreviewUrl = URL.createObjectURL(fileInput.files[0])
      enableImagePlaceholder = false
      deleteAvatar = false
      currentAvatarBase64 = ''
    } else {
      imagePreviewUrl = avatarBase64 ? `data:image/png;base64,${avatarBase64}` : ''
      enableImagePlaceholder = !avatarBase64
      currentAvatarBase64 = avatarBase64
    }
  }

  function resetAvatar() {
    imagePreviewUrl = ''
    enableImagePlaceholder = true
    deleteAvatar = true
    currentAvatarBase64 = ''

    if (fileInput) {
      fileInput.value = ''
    }
  }
</script>

<div class="form-control w-full">
  <div class="flex gap-2">
    <div class="relative flex-shrink-0" style="width: 128px; height: 188px;">
      <div
        class="flex h-full w-full items-center justify-center overflow-hidden rounded transition duration-500"
        style="background-color: {selectedColor};"
      >
        {#if enableImagePlaceholder}
          <span
            class="text-3xl {selectedColor === 'transparent'
              ? 'text-gray-600'
              : 'text-white'}">{altImagePlaceholder.charAt(0)}</span
          >
        {:else}
          <img
            src={imagePreviewUrl}
            alt="Selected avatar"
            class="block"
            style="max-width: 128px; max-height: 188px; width: auto; height: auto;"
          />
        {/if}
      </div>
      {#if !enableImagePlaceholder}
        <button
          type="button"
          class="absolute bottom-2 left-2 z-10 flex h-6 w-6 items-center justify-center rounded-full bg-black bg-opacity-50 p-1 text-xs text-white transition-all hover:bg-opacity-70"
          onclick={resetAvatar}
          aria-label="Reset avatar"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M3 6h18"></path>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          </svg>
        </button>
      {/if}
    </div>
    <div class="flex flex-col">
      <div class="prose prose-sm">{m.assistant_edit_avatar_description()}</div>

      <!-- Color picker -->
      <input type="hidden" name="primary_color" value={selectedColor} />
      <input type="hidden" name="delete_avatar" value={deleteAvatar ? 'true' : 'false'} />
      {#if currentAvatarBase64 && !deleteAvatar}
        <input type="hidden" name="avatar_base64" value={currentAvatarBase64} />
      {/if}
      <ColorPicker {selectedColor} {colors} onColorSelect={handleColorSelect} />

      <div class="mt-4">
        <label for="avatar-upload" class="w-full">
          <input
            bind:this={fileInput}
            id="avatar-upload"
            type="file"
            name="avatar"
            accept="image/png"
            class="file-input file-input-bordered file-input-sm w-full max-w-xs"
            onchange={handleFileChange}
          />
        </label>
        <div class="label pb-0">
          <span class="label-text-alt">{m.assistant_edit_avatar_requirements()}</span>
        </div>
      </div>
    </div>
  </div>
</div>
