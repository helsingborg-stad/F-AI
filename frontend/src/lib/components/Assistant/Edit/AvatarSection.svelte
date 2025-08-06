<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'

  interface Props {
    avatarBase64: string
    altImagePlaceholder: string
    primaryColor: string
  }

  let { avatarBase64, altImagePlaceholder, primaryColor }: Props = $props()

  const colors = [
    'transparent',
    '#e28a8a',
    '#d88bb8',
    '#b18be0',
    '#8ba6e0',
    '#8bd0c6',
    '#9dd990',
    '#f0d27a',
    '#e0bd91',
  ]

  let selectedColor = $state(primaryColor && primaryColor !== '#ffffff' ? primaryColor : colors[Math.floor(Math.random() * (colors.length - 1)) + 1])
  let enableImagePlaceholder = $state(!avatarBase64)
  let imagePreviewUrl = $state(avatarBase64 ? `data:image/png;base64,${avatarBase64}` : '')
  let deleteAvatar = $state(false)
  let fileInput: HTMLInputElement
  let currentAvatarBase64 = $state(avatarBase64)

  function selectColor(color: string) {
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
        class="w-full h-full rounded transition duration-500 overflow-hidden flex items-center justify-center"
        style="background-color: {selectedColor};"
      >
        {#if enableImagePlaceholder}
          <span class="text-3xl {selectedColor === 'transparent' ? 'text-gray-600' : 'text-white'}">{altImagePlaceholder.charAt(0)}</span>
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
          class="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white rounded-full p-1 w-6 h-6 flex items-center justify-center text-xs hover:bg-opacity-70 transition-all z-10"
          onclick={resetAvatar}
          aria-label="Reset avatar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
      <input
        type="hidden"
        name="primary_color"
        value={selectedColor}
      >
      <input
        type="hidden"
        name="delete_avatar"
        value={deleteAvatar ? 'true' : 'false'}
      >
      {#if currentAvatarBase64 && !deleteAvatar}
        <input
          type="hidden"
          name="avatar_base64"
          value={currentAvatarBase64}
        >
      {/if}
      <div class="flex mt-3 ml-1">
        {#each colors as color, i}
          <button
            type="button"
            class="w-10 h-10 rounded-full outline outline-white transition-all relative ml-[-8px] first:ml-0 cursor-pointer hover:z-10 hover:scale-110 overflow-hidden"
            style="{color === 'transparent' ?
              'background: repeating-linear-gradient(45deg, #e5e5e5, #e5e5e5 5px, white 5px, white 10px);' :
              `background-color: ${color};`}
                    {selectedColor === color ?
                      'border: 2px solid white; outline: 2px solid gold; z-index: 5;' :
                      ''}"
            onclick={() => selectColor(color)}
            aria-label={`Select ${color === 'transparent' ? 'transparent' : `color ${i}`}`}
            aria-pressed={selectedColor === color}
          >
            {#if color === 'transparent'}
              <span class="sr-only">Transparent</span>
            {/if}
          </button>
        {/each}
      </div>

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
