<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

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

<div class="flex-none">
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
      <ul class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
        {#each menuItems as menuItem}
          <form action={menuItem.action} method="POST">
            <li>
              <button type="submit"
                      class="flex gap-2 items-center px-4 py-1.5 text-sm cursor-pointer hover:bg-gray-100 rounded-md">
                {menuItem.title}</button>
            </li>
          </form>
        {/each}
      </ul>
    {/if}
  </div>
</div>