<script lang="ts">
  type Props = {
    id: string
    avatar?: string | null
    getAssistantAvatar: (assistantId: string) => Promise<string>
    avatarThumbnail?: string | null
    title: string
    primaryColor: string
    class?: string
  }

  let {
    id,
    avatar,
    avatarThumbnail,
    title,
    primaryColor,
    class: className = '',
    getAssistantAvatar,
  }: Props = $props()

  let isShowingThumbnail = $state(true)
  let displaySrc = $state(avatarThumbnail)

  // Only run this effect when avatar prop changes
  $effect(() => {
    if (avatarThumbnail) {
      // Start with thumbnail and blur
      isShowingThumbnail = true
      displaySrc = avatarThumbnail

      // Preload the full avatar using getAssistantAvatar
      const img = new Image()

      // Using getAssistantAvatar instead of directly setting src
      getAssistantAvatar(id).then(avatarUrl => {
        img.src = avatarUrl
        img.onload = () => {
          // Switch to full avatar and remove blur
          displaySrc = avatarUrl
          isShowingThumbnail = false
        }
      }).catch(() => {
        // If avatar fails to load, remove blur anyway
        isShowingThumbnail = false
      })
    } else {
      // No avatar or avatar is same as thumbnail
      isShowingThumbnail = false
    }
  })
</script>

<div
  class="relative flex items-center justify-center overflow-hidden rounded text-center {className}"
  style="background-color: {primaryColor}"
>
  {#if avatar || avatarThumbnail}
    <img
      class="w-full h-full object-cover transition-all duration-300 {isShowingThumbnail ? 'blur-sm' : ''}"
      src={displaySrc}
      alt="avatar"
    />
  {:else}
    <span
      class="text-3xl {primaryColor === 'transparent'
        ? 'text-gray-600'
        : 'text-white'}"
    >{title.toUpperCase().charAt(0)}
    </span>
  {/if}
</div>