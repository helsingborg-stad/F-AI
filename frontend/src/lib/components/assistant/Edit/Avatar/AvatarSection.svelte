<script lang="ts">
  interface Props {
    avatarBase64: string
    altImagePlaceholder: string
    avatarPrimaryColor: string
  }

  let { avatarBase64, altImagePlaceholder, avatarPrimaryColor }: Props = $props()

  const colors = [
    '#e28a8a',
    '#d88bb8',
    '#b18be0',
    '#8ba6e0',
    '#8bd0c6',
    '#9dd990',
    '#f0d27a',
    '#e0bd91',
  ]

  let selectedColor = $state(avatarPrimaryColor !== '' ?  avatarPrimaryColor : colors[Math.floor(Math.random() * colors.length)])
  let enableImagePlaceholder = $state(!avatarBase64)
  let imagePreviewUrl = $state(`data:image/png;base64,${avatarBase64}`)

  function selectColor(color: string) {
    selectedColor = color
  }

  function handleFileChange(event: Event) {
    const fileInput = event.target as HTMLInputElement

    if (fileInput.files && fileInput.files[0]) {
      imagePreviewUrl = URL.createObjectURL(fileInput.files[0])
      enableImagePlaceholder = false
    } else {
      imagePreviewUrl = ''
      enableImagePlaceholder = true
    }
  }

  function resetAvatar() {
    imagePreviewUrl = ''
    enableImagePlaceholder = true
  }
</script>

<div class="form-control w-full">
  <div class="flex gap-2">
    <div class="avatar relative" class:placeholder={enableImagePlaceholder}>
      <div class="w-32 rounded transition duration-500" style:background-color={selectedColor}>
        {#if enableImagePlaceholder}
          <span class="text-3xl">{altImagePlaceholder.charAt(0)}</span>
        {:else}
          <button
            type="button"
            class="absolute bottom-1 left-1 bg-black bg-opacity-50 text-white rounded-full p-1 w-6 h-6 flex items-center justify-center text-xs hover:bg-opacity-70 transition-all"
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
          <img src={imagePreviewUrl} alt="Selected avatar" />
        {/if}
      </div>
    </div>
    <div class="flex flex-col">
      <div class="prose prose-sm">Upload an image or pick a color to make your assistant unique.</div>

      <!-- Color picker -->
      <input
        type="hidden"
        name="primary_color"
        value={selectedColor}
      >
      <div class="flex mt-3 ml-1">
        {#each colors as color, i}
          <button
            type="button"
            class="w-10 h-10 rounded-full outline outline-white transition-all relative ml-[-8px] first:ml-0 cursor-pointer hover:z-10 hover:scale-110"
            style="background-color: {color};
                    {selectedColor === color ?
                      'border: 2px solid white; outline: 2px solid gold; z-index: 5;' :
                      ''}"
            onclick={() => selectColor(color)}
            aria-label={`Select color ${i+1}`}
            aria-pressed={selectedColor === color}
          ></button>
        {/each}
      </div>

      <div class="mt-4">
        <label for="avatar-upload" class="w-full">
          <input
            id="avatar-upload"
            type="file"
            name="avatar"
            accept="image/png"
            class="file-input file-input-bordered file-input-sm w-full max-w-xs"
            onchange={handleFileChange}
          />
        </label>
        <div class="label pb-0">
          <span class="label-text-alt">Upload a square image for best results (max 1MB)</span>
        </div>
      </div>
    </div>
  </div>
</div>