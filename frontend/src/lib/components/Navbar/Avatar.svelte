<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import VerticalDivider from '$lib/components/Divider/VerticalDivider.svelte'

  interface Props {
    avatarUrl: string
    avatarPlaceholder: string
    menuItems: [{
      title: string
      action: string
    }]
  }

  let { avatarUrl, avatarPlaceholder, menuItems }: Props = $props()
</script>


<div class="dropdown dropdown-end">
  {#if avatarUrl}
    <div tabindex="0" role="button" class="avatar btn btn-circle btn-ghost">
      <div class="w-10 rounded-full">
        <img src={avatarUrl.toString()} alt="Profile" />
      </div>
    </div>
  {:else}
    <div tabindex="0" role="button" class="avatar placeholder btn btn-sm btn-circle btn-ghost">
      <div class="bg-neutral-300 text-base w-10 rounded-full">
        {#if avatarPlaceholder}
          <span>{avatarPlaceholder.charAt(0).toUpperCase()}</span>
        {:else}
          <Icon icon={icons["circleUser"]} />
        {/if}
      </div>
    </div>
  {/if}
  {#if menuItems}
    <ul class="dropdown-content menu gap-1 bg-base-100 rounded-lg z-[30] min-w-64 p-2 shadow">
      <div class="text-gray-500 py-1 px-2 overflow-ellipsis select-none">
        {avatarPlaceholder}
      </div>
      <li>
        <button class="flex mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md">
          Language
        </button>
      </li>
      {#each menuItems as menuItem}
        <form action={menuItem.action} method="POST">
          <li>
            <button
              type="submit"
              class="flex mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md">
              {menuItem.title}</button>
          </li>
        </form>
      {/each}
    </ul>
  {/if}
</div>
