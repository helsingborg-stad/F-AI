<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    title?: string;
    canCreateAssistant?: boolean;
  }

  const { title = 'Assistants', canCreateAssistant = false }: Props = $props()
</script>

<div class="py-2 px-8">
  <div class="flex flex-row justify-between">
    <p class="text-xl font-medium">{title}</p>
    {#if canCreateAssistant}
      <button class="btn btn-sm btn-success text-white">
        <Icon icon={icons["userPlus"]} width={20} height={20} />
        <span class="text-s">Create</span>
      </button>
    {/if}
  </div>
</div>