<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'

  interface Props {
    canEdit: boolean
    canDelete: boolean
    canCreate: boolean
    onDelete: () => void
    onCopy: () => void
    onUpdate: () => void
  }

  let { canEdit, canCreate, onDelete, onCopy, onUpdate }: Props = $props()
</script>

{#if canEdit}
  <div class="flex justify-between">
    <div class="flex flex-row gap-2">
      <div>
        <button type="submit" class="btn btn-error btn-sm text-white" onclick={onDelete}>
          <Icon icon={icons['trash']} width={20} height={20} />
        </button>
      </div>
      {#if canCreate}
        <div>
          <button
            type="submit"
            class="btn btn-sm bg-gray-400 text-white"
            onclick={onCopy}
          >
            <Icon icon={icons['copy']} width={20} height={20} />
          </button>
        </div>
      {/if}
    </div>
    <div>
      <button type="submit" class="btn btn-success btn-sm text-white" onclick={onUpdate}>
        <Icon icon={icons['save']} width={20} height={20} />
        <span class="text-s">{m.common_action_save()}</span>
      </button>
    </div>
  </div>
{/if}
