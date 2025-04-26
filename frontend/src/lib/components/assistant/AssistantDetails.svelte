<script lang="ts">
  import type { IAssistant } from '$lib/types.js'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'

  interface Props {
    assistant?: IAssistant
    canEdit?: boolean
  }

  let {
    assistant,
    canEdit = false,
  }: Props = $props()
</script>

{#if assistant}
  <p>Assistant details</p>
  <div class="flex flex-col">
    <form method="POST" action="?/update">
      <input
        type="hidden"
        name="assistant_id"
        value={assistant.id}
      />

      <label class="form-control w-full max-w-xs">
        <div class="label">
          <span class="label-text">Name</span>
        </div>
        <input
          type="text"
          name="name"
          placeholder="Enter a user friendly name"
          class="input input-bordered input-sm w-full max-w-xs"
          value={assistant.name}
        />
        <div class="label">
          <span class="label-text-alt opacity-50">{assistant.id}</span>
        </div>
      </label>

      <label class="form-control">
        <div class="label">
          <span class="label-text">System instructions</span>
        </div>
        <textarea
          name="instructions"
          class="textarea textarea-bordered h-24"
          placeholder="You are a helpful assistant...">{assistant.instructions}</textarea>
      </label>

      <label class="form-control w-full max-w-xs">
        <div class="label">
          <span class="label-text">Model</span>
        </div>
        <select class="select select-bordered select-sm text-sm">
          <option>gpt-4</option>
        </select>
      </label>

      <div>
        <div class="opacity-50">Tools</div>
        <HorizontalDivider />
        <div class="flex flex-row">
          <input type="checkbox" class="toggle toggle-sm toggle-success" />
          <p>File search</p>
        </div>
        <HorizontalDivider />
        <div class="flex flex-row">
          <p>Functions</p>
        </div>
      </div>

    </form>
  </div>
{/if}