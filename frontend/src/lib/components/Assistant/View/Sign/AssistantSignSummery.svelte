<script lang="ts">
  import type { IAssistantCard } from '$lib/types.js'
  import AssistantSign from '$lib/components/Assistant/View/Sign/AssistantSign.svelte'

  let { id, avatar, primaryColor, title, description, owner, starters, isFavorite, metadata }: IAssistantCard = $props()
  let dialog: HTMLDialogElement

  const height = 'h-24'
  const maxHeight = `max-${height}`

  let onClick = () => {
    dialog.showModal()
  }
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
  {#if !avatar}
    <div
      class="w-20 flex items-center justify-center relative rounded overflow-hidden text-center"
      style="background-color: {primaryColor}"
    >
      <span
        class="{maxHeight} w-20 text-3xl {primaryColor === 'transparent' ? 'text-gray-600' : 'text-white'}">{title.toUpperCase().charAt(0)}
      </span>
    </div>
  {:else}
    <figure>
      <img
        class="{maxHeight} w-20"
        src={avatar}
        alt="avatar" />
    </figure>
  {/if}
  <div class="card-body">
    <div class="card-title font-semibold md:text-lg">{title}</div>
    <p>{description}</p>
  </div>
</div>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box w-11/12 max-w-xl">
    <AssistantSign {id} {avatar} {title} {owner} {description} {isFavorite} {metadata} {starters} />
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
