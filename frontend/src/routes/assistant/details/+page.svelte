<script lang="ts">
  import SetAssistantAvatar from '$lib/components/assistant/SetAssistantAvatar.svelte'
  import { userState } from '$lib/state/user.svelte.js'

  let { data } = $props()

  const { assistant, models } = data
  let selectedModelKey = $state(assistant.model)

  let processingDelete = $state(false)
  let processingUpdate = $state(false)
  let disableFormButtons = $derived(processingUpdate || processingDelete)

  function handleDelete() {
    processingDelete = true
  }

  function handleUpdate() {
    processingUpdate = true

    return () => {
      processingUpdate = false
      processingDelete = false
    }
  }
</script>

<p>Assistant details</p>
<div class="flex w-full justify-between p-4 gap-2">
  <SetAssistantAvatar />
  <div class="basis-5/6">
    <div class="flex flex-col w-full justify-between gap-4">
      <div class="flex flex-col w-full justify-between gap-2">
        <form method="POST" action="?/update" onsubmit={handleUpdate}>
          <label class="form-control w-full max-w-xs">
            <input type="hidden" name="assistant_id" value={assistant.id} />
            <input type="hidden" name="model_key" bind:value={selectedModelKey} />
            <div class="label">
              <span class="label-text">Assistant name</span>
            </div>
            <input
              class="input input-sm input-bordered w-full max-w-xs"
              name="name"
              type="text"
              autocomplete="off"
              required
              value={assistant.name}
            />
          </label>
          <select
            class="select select-sm select-bordered w-full max-w-xs"
            name="model"
            required
            bind:value={selectedModelKey}
          >
            <option value="" disabled selected>Select a model</option>
            {#each models as model}
              <option value="{model.key}">{model.name}</option>
            {/each}
          </select>
          <label class="form-control">
            <div class="label">
              <span class="label-text">Instructions</span>
            </div>
            <textarea
              class="textarea textarea-bordered h-24"
              name="instructions"
            >{assistant.instructions}</textarea>
            <div class="label">
              <span class="label-text">Description</span>
            </div>
            <textarea
              class="textarea textarea-bordered h-24"
              name="description"
            >{assistant.description}</textarea>
          </label>
          {#if assistant.owner === userState.email}
            <button type="submit" class="btn btn-block mt-2 btn-warning" disabled={disableFormButtons}>
              Update assistant
              {#if processingUpdate}
                <span class="loading loading-spinner"></span>
              {/if}
            </button>
          {/if}
        </form>
        {#if assistant.owner === userState.email}
          <form method="POST" action="?/delete" onsubmit={handleDelete}>
            <input type="hidden" name="assistant_id" value={assistant.id} />
            <button type="submit" class="btn btn-block btn-error" disabled={disableFormButtons}>
              Delete assistant
              {#if processingDelete}
                <span class="loading loading-spinner"></span>
              {/if}
            </button>
          </form>
        {/if}
      </div>
    </div>
  </div>
</div>