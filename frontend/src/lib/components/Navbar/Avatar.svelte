<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import { setLocale, type Locale, getLocale } from '$lib/paraglide/runtime.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    avatarUrl: string
    avatarPlaceholder: string
    menuItems: [
      {
        title: string
        action: string
      },
    ]
  }

  let { avatarUrl, avatarPlaceholder, menuItems }: Props = $props()

  let showLanguageMenu = $state(false)
  let currentLocale = getLocale()

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'sv', name: 'Svenska' },
    { code: 'fr', name: 'Français' },
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
    <div
      tabindex="0"
      role="button"
      class="avatar placeholder btn btn-circle btn-ghost btn-sm"
    >
      <div class="w-10 rounded-full bg-neutral-300 text-base">
        {#if avatarPlaceholder}
          <span>{avatarPlaceholder.charAt(0).toUpperCase()}</span>
        {:else}
          <Icon icon={icons['circleUser']} />
        {/if}
      </div>
    </div>
  {/if}
  {#if menuItems}
    <ul
      class="menu dropdown-content z-[30] min-w-64 gap-1 rounded-lg bg-base-100 p-2 shadow"
    >
      <li tabindex="-1" class="pointer-events-none">
        <div class="select-none overflow-ellipsis px-2 py-1 text-gray-500">
          {avatarPlaceholder}
        </div>
      </li>
      <div class="dropdown dropdown-left mr-1 pr-2">
        <button
          tabindex="0"
          class="mx-2 flex w-full items-center gap-2 rounded-md p-1 pr-2 text-sm hover:bg-gray-100"
          onclick={() => (showLanguageMenu = !showLanguageMenu)}
        >
          {m.nav_menu_language()}
        </button>
        {#if showLanguageMenu}
          <ul class="menu dropdown-content z-[1] w-52 rounded-lg bg-base-100 p-2 shadow">
            {#each languages as lang}
              <li>
                <button
                  class:active={lang.code === currentLocale}
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
              class="mx-2 flex items-center gap-2 rounded-md p-1 text-sm hover:bg-gray-100"
            >
              {menuItem.title}
            </button>
          </li>
        </form>
      {/each}
    </ul>
  {/if}
</div>
