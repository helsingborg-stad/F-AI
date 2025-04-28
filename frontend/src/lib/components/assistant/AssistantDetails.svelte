<script lang="ts">
  import type { IAssistant } from '$lib/types.js'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'

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
  <div class="flex flex-col gap-y-4">
    <form method="POST" action="?/update" class="space-y-4">
      <input
        type="hidden"
        name="assistant_id"
        value={assistant.id}
      />

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text">Name</span>
        </div>
        <input
          type="text"
          name="name"
          placeholder="Enter a user friendly name"
          class="input input-bordered input-sm w-full"
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

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text">Model</span>
        </div>
        <select class="select select-bordered select-sm text-sm">
          <option>gpt-4</option>
          <option>claud</option>
        </select>
      </label>

      <div class="space-y-2 pt-5">
        <div class="opacity-50 pb-2">Tools</div>
        <HorizontalDivider />
        <div class="flex flex-row place-content-between items-center">
          <div class="flex flex-row gap-2">
            <input type="checkbox" class="toggle toggle-sm toggle-success" />
            <InfoTooltip
              toolTip="File Search enables the assistant with knowledge from files that you or your users upload.">
              <div class="text-sm font-medium select-none">File search</div>
            </InfoTooltip>
          </div>
          <div>
            <button class="btn btn-sm">
              <Icon icon={icons["settings"]} width={16} height={16} />
            </button>
            <button class="btn btn-sm">
              <Icon icon={icons["plus"]} width={16} height={16} />
              <span class="text-s">Files</span>
            </button>
          </div>
        </div>
        <HorizontalDivider />
        <div class="flex flex-row place-content-between items-center">
          <div>
            <InfoTooltip
              toolTip="Function calling lets you describe custom functions of your app or external APIs to the assistant.">
              <div class="text-sm font-medium">Functions</div>
            </InfoTooltip>
          </div>
          <div>
            <button class="btn btn-sm">
              <Icon icon={icons["plus"]} width={16} height={16} />
              <span class="text-s">Functions</span>
            </button>
          </div>
        </div>
      </div>

      <div class="pt-5">
        <div class="opacity-50 pb-2">Model configuration</div>
        <HorizontalDivider />
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Response format</span>
          </div>
          <select class="select select-bordered select-sm text-sm">
            <option>text</option>
            <option>json_format</option>
          </select>
        </label>

      </div>


    </form>
  </div>
{/if}