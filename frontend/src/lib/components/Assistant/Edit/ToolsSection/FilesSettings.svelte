<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { fade } from 'svelte/transition'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  const DEFAULT_RESULTS = 10

  interface Props {
    maxCollection: string
  }

  let { maxCollection }: Props = $props()

  let maxCollectionResults = $state(Number(maxCollection))

  function reset() {
    maxCollectionResults = DEFAULT_RESULTS
  }
</script>

<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="btn btn-sm">
    <Icon icon={icons['settings']} width={16} height={16} />
  </div>

  <div
    role="dialog"
    aria-label={m.assistant_edit_tools_arial_label_file()}
    class="card dropdown-content card-compact z-[1] w-64 bg-white p-2 shadow"
  >
    <div class="card-body">
      <div class="flex flex-row place-content-between items-center">
        <div class="select-none text-sm font-medium">
          {m.assistant_edit_tools_file_max_result()}
        </div>
        <div class="flex flex-row items-center gap-1">
          {#if maxCollectionResults !== DEFAULT_RESULTS}
            <button
              type="button"
              class="btn btn-ghost btn-xs bg-inherit"
              transition:fade={{ duration: 200, delay: 500 }}
              onmousedown={(e) => {
                e.preventDefault()
                reset()
              }}
            >
              <Icon icon={icons['rotateCcw']} width={16} height={16} />
            </button>
          {/if}
          <div
            class="flex h-8 w-8 select-none items-center justify-center font-mono text-sm"
          >
            {maxCollectionResults}
          </div>
        </div>
      </div>
      <input
        type="range"
        name="max_collection_results"
        min="0"
        max="30"
        bind:value={maxCollectionResults}
        class="range range-xs"
      />
      <div class="select-none pt-2 text-xs opacity-50">
        {m.assistant_edit_tools_file_user_info()}
      </div>
    </div>
  </div>
</div>
