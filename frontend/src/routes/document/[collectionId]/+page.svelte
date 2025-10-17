<script lang="ts">
  import type { PageProps } from './$types.js'
  import { m } from '$lib/paraglide/messages.js'
  import type { ICollection } from '$lib/types.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  const { data }: PageProps = $props()
  const collection: ICollection = $derived(data.collection)
</script>

<div class="flex flex-col gap-5 p-10">
  <form method="post" action="?/changeLabel">
    <div class="flex items-center justify-center gap-1">
      <label class="form-control text-sm" for="name">Name</label>
      <input
        type="text"
        name="label"
        placeholder="e.g. 'Shakespeare works'"
        class="input input-sm input-bordered w-full"
        bind:value={collection.label}
        readonly={false}
        autocomplete="off"
        onkeydown={(e) => e.key === 'Enter' && e.preventDefault()}
      />
      <button type="submit" class="btn btn-success btn-sm text-white">
        <Icon icon={icons['save']} width={20} height={20} />
        <span class="text-s">{m.common_action_save()}</span>
      </button>
    </div>
  </form>
  <h2 class="text-xl font-bold">Documents</h2>
  <div class="grid grid-cols-3 gap-2">
    {#each collection.documents as document (document.name)}
      <span>{document.name}</span>
      <span>{document.type}</span>
      <span>{document.state}</span>
    {:else}
      <span class="col-span-3 text-sm">
        This document collection is empty. Add documents below.
      </span>
    {/each}
  </div>

  <form method="post" action="?/changeDocuments" enctype="multipart/form-data">
    <input
      name="files"
      type="file"
      class="file-input file-input-sm w-full max-w-xs"
      multiple
      required
    />
    <button type="submit" class="btn btn-success btn-sm text-white"
      >Change Documents
    </button>
  </form>
</div>
