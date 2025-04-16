<script lang="ts">
  import SetAssistantAvatar from '$lib/components/assistant/SetAssistantAvatar.svelte'
  import type { IAssistantModels } from '$lib/types.js'

  let { data }: IAssistantModels = $props()

  const availableModels = data.models
  let selectedModelKey = $state('')
</script>

<p>Create new assistant</p>
<div class="flex w-full justify-between p-4 gap-2">
  <SetAssistantAvatar />
  <div class="basis-5/6">
    <div class="flex flex-col w-full justify-between gap-4">
      <form method="POST" action="?/create">
        <div class="flex flex-col w-full justify-between gap-2">
          <label class="form-control w-full max-w-xs">
            <input
              type="hidden"
              name="model_key"
              bind:value={selectedModelKey}
            >
            <div class="label">
              <span class="label-text">Assistant name</span>
            </div>
            <input
              class="input input-sm input-bordered w-full max-w-xs"
              name="name"
              type="text"
              autocomplete="off"
              required
            />
          </label>
          <select
            class="select select-sm select-bordered w-full max-w-xs"
            name="model"
            required
            bind:value={selectedModelKey}
          >
            <option value="" disabled selected>Select a model</option>
            {#each availableModels as model}
              <option value={model.key}>{model.name}</option>
            {/each}
          </select>
          <label class="form-control">
            <div class="label">
              <span class="label-text">Instructions</span>
            </div>
            <textarea
              class="textarea textarea-bordered h-24"
              name="instructions"
            ></textarea>
            <div class="label">
              <span class="label-text">Description</span>
            </div>
            <textarea
              class="textarea textarea-bordered h-24"
              name="description"
            ></textarea>
          </label>
          <button class="btn">Create assistant</button>
        </div>
      </form>
    </div>
  </div>
</div>
