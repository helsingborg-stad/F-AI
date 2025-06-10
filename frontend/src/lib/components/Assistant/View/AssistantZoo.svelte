<script lang="ts">
  import type { IExhibit } from '$lib/types.js'
  import Exhibit from '$lib/components/Assistant/View/Exhibit.svelte'
  import SearchBar from '$lib/components/Assistant/View/SearchBar.svelte'

  interface Props {
    exhibits: IExhibit[]
  }

  let { exhibits }: Props = $props()

  let filter = $state('')

  let filteredExhibits = $derived(
    exhibits
      .map(exhibit => ({
        ...exhibit,
        cards: exhibit.cards.filter(card =>
          card.title.toLowerCase().includes(filter.toLowerCase()) ||
          card.description.toLowerCase().includes(filter.toLowerCase())
        )
      }))
      .filter(exhibit => exhibit.cards.length > 0)
  )
</script>

<div class="h-full overflow-y-auto">
  <div class="mb-24">
    <SearchBar bind:value={filter} />
  </div>
  <div class="w-full mx-auto max-w-3xl px-4">
    {#each filteredExhibits as exhibit}
      <Exhibit
        title={exhibit.title}
        description={exhibit.description}
        cards={exhibit.cards}
      />
    {/each}
  </div>
</div>