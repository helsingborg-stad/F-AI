<script lang="ts">
  import AssistantCard from '$lib/components/Assistant/View/AssistantCard.svelte'
  import type { IExhibit } from '$lib/types.js'

  let { title, description, cards }: IExhibit = $props()
</script>

<div class="text-xl font-semibold">{title}</div>
<div class="text-sm text-gray-500">{description}</div>
<div class="mt-4 mb-10">
  <div class="grid grid-cols-1 gap-x-1.5 gap-y-1 lg:grid-cols-2 lg:gap-x-3 lg:gap-y-2.5">
    {#each cards as card}
      <AssistantCard
        avatar={card.avatar}
        title={card.title}
        description={card.description}
      />
    {/each}
  </div>
</div>
