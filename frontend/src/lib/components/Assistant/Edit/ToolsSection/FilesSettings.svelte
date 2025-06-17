<script lang="ts">
  import { fade } from 'svelte/transition'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  const DEFAULT_RESULTS = '10'

  interface Props {
    maxCollection: string
  }

  let { maxCollection }: Props = $props()

  let maxCollectionResults = $state(maxCollection)

  function reset() {
    maxCollectionResults = DEFAULT_RESULTS
  }
</script>

<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="btn btn-sm">
    <Icon icon={icons["settings"]} width={16} height={16} />
  </div>

  <div
    role="dialog"
    aria-label="File settings"
    class="dropdown-content card card-compact bg-white z-[1] w-64 p-2 shadow">
    <div class="card-body">
      <div class="flex flex-row place-content-between items-center">
        <div class="text-sm font-medium select-none">Max results</div>
        <div class="flex flex-row items-center gap-1">
          {#if maxCollectionResults !== DEFAULT_RESULTS}
            <button
              type="button"
              class="btn btn-ghost btn-xs bg-inherit"
              transition:fade={{ duration: 200, delay: 500 }}
              onmousedown={(e) => {
                e.preventDefault()
                reset()
              }}>
              <Icon icon={icons["rotateCcw"]} width={16} height={16} />
            </button>
          {/if}
          <div
            class="text-sm select-none w-8 h-8 font-mono flex items-center justify-center">{maxCollectionResults}</div>
        </div>
      </div>
      <input
        type="range"
        name="maxCollectionResults"
        min="0"
        max="30"
        bind:value={maxCollectionResults}
        class="range range-xs"
      />
      <div class="pt-2 text-xs opacity-50 select-none">Set the max results to retrieve from files. High numbers (>10)
        may
        increase accuracy but also takes longer to process.
      </div>
    </div>
  </div>
</div>
