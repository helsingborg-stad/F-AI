<script lang="ts">
  import type { IAssistant } from '$lib/types.js'

  interface Props {
    assistants: IAssistant[]
    activeAssistant?: IAssistant
  }

  let { assistants, activeAssistant = {} }: Props = $props()
</script>


<div class="overflow-x-auto">
  <table class="table">
    <tbody>
    {#each assistants as assistant}
      <tr class="hover" class:bg-base-200={activeAssistant.id === assistant.id}>
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