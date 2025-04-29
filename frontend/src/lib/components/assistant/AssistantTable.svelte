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
            <div class="text-base">{assistant.name}</div>
            <div class="text-xs opacity-50">{assistant.id}</div>
          </div>
        </td>
      </tr>
    {/each}
    </tbody>
  </table>
</div>