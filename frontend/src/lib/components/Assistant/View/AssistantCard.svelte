<script lang="ts">
  import type { IAssistantCard } from '$lib/types.js'

  let { avatar, title, description }: IAssistantCard = $props()

  const height = 'h-24'
  const maxHeight = `max-${height}`

  let onClick: () => void
</script>

<div
  class="card card-compact card-side {height} hover:bg-gray-100 cursor-pointer"
  onclick={onClick}
  onkeydown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick?.()
    }
  }}
  role="button"
  tabindex="0"
>
  <figure>
    <img
      class="{maxHeight} w-20"
      src={avatar}
      alt="avatar" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{title}</h2>
    <p>{description}</p>
  </div>
</div>