<script lang="ts">
  import type { IAssistant } from '$lib/types.js'

  interface Props {
    assistants: IAssistant[]
    activeAssistant?: IAssistant
  }

  let { assistants, activeAssistant = {} }: Props = $props()

  function handleAssistantClick(assistant: IAssistant) {
    const url = new URL(window.location.href)
    url.searchParams.set('assistant_id', assistant.id)
    window.location.href = url.toString()
  }
</script>

<div class="overflow-x-auto pt-4">
  <table class="table">
    <tbody>
    {#each assistants as assistant}
      <tr
        class="hover"
        class:bg-base-200={activeAssistant.id === assistant.id}
        onclick={() => handleAssistantClick(assistant)}
        role="button"
        tabindex="0"
      >
        <td>
          <div class="flex flex-col">
            {#if assistant.avatar_base64}
              <img src={`data:image/png;base64,${assistant.avatar_base64}`} alt="avatar"
                   class="w-10 h-10 bg-white object-contain p-2" />
            {/if}
            <div class="text-base">{assistant.name ? assistant.name : 'Untitled assistant'}</div>
            <div class="text-xs opacity-50">{assistant.id}</div>
          </div>
        </td>
      </tr>
    {/each}
    </tbody>
  </table>
</div>