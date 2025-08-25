<script lang="ts">
  import AssistantSignSummery from '$lib/components/Assistant/View/Sign/AssistantSignSummery.svelte'
  import type { IExhibit } from '$lib/types.js'

  let { title, description, cards }: IExhibit = $props()

  let openedId = $state('')

  $effect(() => {
    openedId = new URL(window.location.href).searchParams.get('id') ?? ''
  })
</script>

<div class="pb-8">
  <div class="text-xl font-semibold md:text-2xl">{title}</div>
  <div class="text-sm text-gray-500">{description}</div>
  <div class="mb-10 mt-4">
    <div
      class="grid grid-cols-1 gap-x-1.5 gap-y-1 lg:grid-cols-2 lg:gap-x-3 lg:gap-y-2.5"
    >
      {#each cards as card}
        <AssistantSignSummery
          id={card.id}
          avatar={card.avatar}
          primaryColor={card.primaryColor}
          title={card.title}
          description={card.description}
          owner={card.owner}
          isFavorite={card.isFavorite}
          starters={card.starters}
          metadata={card.metadata}
          dialogOpen={openedId === card.id}
        />
      {/each}
    </div>
  </div>
</div>
