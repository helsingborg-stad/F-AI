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

  $effect(() => {
    if (avatarThumbnail) {
      isShowingThumbnail = true
      displaySrc = avatarThumbnail

      const img = new Image()

      getAssistantAvatar(id).then(avatarUrl => {
        img.src = avatarUrl
        img.onload = () => {
          displaySrc = avatarUrl
          isShowingThumbnail = false
        }
      }).catch(() => {
        isShowingThumbnail = false
      })
    } else {
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