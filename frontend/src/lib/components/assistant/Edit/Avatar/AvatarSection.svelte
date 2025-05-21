<script lang="ts">
  interface Props {
    placeholderCharacter: string
    avatarColor?: string
  }

  let { placeholderCharacter, avatarColor }: Props = $props()

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

  let selectedColor = $state(avatarColor || colors[Math.floor(Math.random() * colors.length)])
  let enableAvatarPlaceholder = $state(true)

  function selectColor(color: string) {
    selectedColor = color
  }
</script>

<div class="form-control w-full">
  <div class="flex gap-2">
    <div class="avatar" class:placeholder={enableAvatarPlaceholder}>
      <div class="w-32 rounded transition duration-500" style:background-color={selectedColor}>
        {#if enableAvatarPlaceholder}
          <span class="text-3xl">{placeholderCharacter.charAt(0)}</span>
        {:else}
          <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" alt="avatar" />
        {/if}
      </div>
    </div>
    <div class="flex flex-col">
      <div class="prose prose-sm">Upload an image or pick a color to make your assistant unique.</div>

      <!-- Color picker -->
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
            accept="image/*"
            class="file-input file-input-bordered file-input-sm w-full max-w-xs"
          />
        </label>
        <div class="label pb-0">
          <span class="label-text-alt">Upload a square image for best results (max 1MB)</span>
        </div>
      </div>
    </div>
  </div>
</div>