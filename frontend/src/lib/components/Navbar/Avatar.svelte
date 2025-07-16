<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'
  import { setLocale, type Locale } from '$lib/paraglide/runtime.js'
  import { getLocale } from '../../../paraglide/runtime.js'

  interface Props {
    avatarUrl: string
    avatarPlaceholder: string
    menuItems: [{
      title: string
      action: string
    }]
  }

  let {
    avatarUrl,
    avatarPlaceholder,
    menuItems,
  }: Props = $props()

  let showLanguageMenu = $state(false)

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'sv', name: 'Swedish', flag: '🇸🇪' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
  ]

  function handleSetLanguage(languageCode: string) {
    setLocale(languageCode as Locale)
  }
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
      <li>
        <div class="text-gray-500 py-1 px-2 overflow-ellipsis select-none">
          {avatarPlaceholder}
        </div>
      </li>
      <div class="dropdown dropdown-left pr-2 mr-1">
        <button
          tabindex="0"
          class="flex w-full mx-2 p-1 pr-2 gap-2 items-center text-sm hover:bg-gray-100 rounded-md"
          onclick={() => showLanguageMenu = !showLanguageMenu}
        >
          Lang
        </button>
        {#if showLanguageMenu}
          <ul class="menu dropdown-content bg-base-100 rounded-lg z-[1] w-52 p-2 shadow">
            {#each languages as lang}
              <li>
                <button
                  onclick={() => handleSetLanguage(lang.code)}
                >
                  {lang.name}
                </button>
              </li>
            {/each}
          </ul>
        {/if}
      </div>

      {#each menuItems as menuItem}
        <form action={menuItem.action} method="POST">
          <li>
            <button
              type="submit"
              class="flex mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md">
              {menuItem.title}
            </button>
          </li>
        </form>
      {/each}
    </ul>
  {/if}
</div>
