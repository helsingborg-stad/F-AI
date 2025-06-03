<script lang="ts">
  import { enhance } from '$app/forms'

  interface Props {
    id: string
    isFavorite: boolean
  }

  let { id, isFavorite }: Props = $props()

  let enable = $state(isFavorite)
</script>

<form method="POST" action="?/toggleFavorite" use:enhance={() => {
  // Optimistic UI update
  return async ({ result }) => {
    if (result.type === 'failure') {
      enable = !enable;
    }
  };
}}>
  <input type="hidden" name="itemId" value={id} />

  <label class="swap swap-rotate">
    <input
      type="checkbox"
      name="isFavorite"
      checked={enable}
      onchange={(e) => e.currentTarget?.form?.requestSubmit()}
    />

    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="swap-on lucide lucide-star-icon lucide-star text-yellow-400 fill-yellow-400">
      <path
        d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z" />
    </svg>

    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="swap-off lucide lucide-star-off-icon lucide-star-off">
      <path d="M8.34 8.34 2 9.27l5 4.87L5.82 21 12 17.77 18.18 21l-.59-3.43" />
      <path d="M18.42 12.76 22 9.27l-6.91-1L12 2l-1.44 2.91" />
      <line x1="2" x2="22" y1="2" y2="22" />
    </svg>
  </label>
</form>
