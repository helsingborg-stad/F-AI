<script lang="ts">
  import { onMount } from 'svelte'
  import { m } from '$lib/paraglide/messages.js'
  import type { IAssistantMenu } from '$lib/types.js'

  interface Props {
    assistants: IAssistantMenu[]
    selectedAssistantId: string
    disabled: boolean
  }

  let { assistants, selectedAssistantId = $bindable(), disabled }: Props = $props()

  let isOpen = $state(false)
  let dropdownRef: HTMLDivElement = $state(undefined as unknown as HTMLDivElement)

  function selectAssistant(assistant: { id: string, name: string }) {
    selectedAssistantId = assistant.id
    isOpen = false
  }

  function toggleDropdown() {
    isOpen = !isOpen
  }

  const selectedAssistantName = $derived(
    !selectedAssistantId
      ? m.chat_assistant_picker_select()
      : assistants
        .flatMap(group => group.menuItems)
        .find(item => item.id === selectedAssistantId)?.name ||
      (disabled ? m.chat_assistant_picker_unknown() : m.chat_assistant_picker_select()),
  )

  function handleClickOutside(event: MouseEvent) {
    if (isOpen && dropdownRef && !dropdownRef.contains(event.target as Node)) {
      isOpen = false
    }
  }

  onMount(() => {
    document.addEventListener('click', handleClickOutside)

    return () => {
      document.removeEventListener('click', handleClickOutside)
    }
  })
</script>

{#if disabled}
  <button class="btn btn-sm btn-ghost m-1 pointer-events-none cursor-not-allowed">
    {selectedAssistantName}
  </button>
{:else}
  <div class="dropdown dropdown-top dropdown-end dropdown-open" bind:this={dropdownRef}>
    <button
      class="btn btn-sm btn-ghost m-1"
      aria-haspopup="true"
      aria-expanded={isOpen}
      aria-controls="dropdown-menu"
      onclick={(e) => {
        e.stopPropagation();
        toggleDropdown();
      }}
      onkeydown={(e) => e.key === 'Enter' && toggleDropdown()}
    >
      {selectedAssistantName}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="ml-1 {isOpen ? 'rotate-180' : ''} transition-transform duration-300"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>
    <ul
      id="dropdown-menu"
      class="dropdown-content menu bg-base-100 rounded-md z-[999] w-52 p-2 shadow"
      class:hidden={!isOpen}
      role="menu"
    >
      {#each assistants.filter(item => !item.hidden) as item}
        {#if item.menuTitle}
          <div class="pt-1">{item.menuTitle}</div>
        {/if}
        {#each item.menuItems as menuItem}
          <li role="menuitem">
            <button
              class={selectedAssistantId === menuItem.id ? 'active' : ''}
              onclick={(e) => {
                e.stopPropagation();
                selectAssistant(menuItem);
              }}
            >
              {menuItem.name}
            </button>
          </li>
        {/each}
      {/each}
    </ul>
  </div>
{/if}
