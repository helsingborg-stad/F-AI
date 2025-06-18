<script lang="ts">
  import AssistantSignSummery from '$lib/components/Assistant/View/Sign/AssistantSignSummery.svelte'
  import type { IExhibit } from '$lib/types.js'

  let { title, description, cards }: IExhibit = $props()
</script>

<div class="pb-8">
  <div class="text-xl font-semibold md:text-2xl">{title}</div>
  <div class="text-sm text-gray-500">{description}</div>
  <div class="mt-4 mb-10">
    <div class="grid grid-cols-1 gap-x-1.5 gap-y-1 lg:grid-cols-2 lg:gap-x-3 lg:gap-y-2.5">
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
        />
      {/each}
    </div>
  </div>
</div>
