<script lang="ts">
  import type { IAssistantCard } from '$lib/types.js'
  import AssistantSign from '$lib/components/Assistant/View/Sign/AssistantSign.svelte'

  type Props = IAssistantCard & {
    dialogOpen: boolean
  }

  let {
    id,
    avatar,
    primaryColor,
    title,
    description,
    owner,
    starters,
    isFavorite,
    metadata,
    dialogOpen = $bindable(),
  }: Props = $props()
  let dialog: HTMLDialogElement

  const height = 'h-24'
  const maxHeight = `max-${height}`

  let onClick = () => {
    dialogOpen = true
  }

  $effect(() => {
    if (dialogOpen !== dialog.open) {
      if (dialogOpen) {
        dialog.showModal()
      } else {
        dialog.close()
      }
    }
  })
</script>

<div
  class="card card-side card-compact {height} cursor-pointer hover:bg-gray-100"
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
  <div
    class="relative flex items-center justify-center overflow-hidden rounded text-center w-20 shrink-0 {maxHeight}"
    style="background-color: {primaryColor}"
  >
    {#if avatar}
      <img class="w-full h-full object-cover" src={avatar} alt="avatar" />
    {:else}
      <span
        class="text-3xl {primaryColor === 'transparent'
          ? 'text-gray-600'
          : 'text-white'}"
      >{title.toUpperCase().charAt(0)}
      </span>
    {/if}
  </div>
  <div class="card-body">
    <div class="card-title font-semibold md:text-lg">{title}</div>
    <p>{description}</p>
  </div>
</div>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box w-11/12 max-w-xl">
    <AssistantSign
      {id}
      {avatar}
      {title}
      {owner}
      {description}
      {isFavorite}
      {metadata}
      {starters}
    />
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>