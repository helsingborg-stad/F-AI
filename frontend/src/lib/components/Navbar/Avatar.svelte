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

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'sv', name: 'Swedish', flag: '🇸🇪' },
  ]

  let currentLanguage = 'en'
  let showLanguageMenu = $state(false)

  let dropdownRef: HTMLDivElement = $state(undefined as unknown as HTMLDivElement)
  let isOpen = $state(false)

  function selectLanguage(langCode: string) {
    // Set language logic
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
      <li>
        <!--        <button-->
        <!--          class="flex mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md"-->
        <!--          onclick={() => showLanguageMenu = !showLanguageMenu}-->
        <!--        >-->
        <!--          Language-->
        <!--        </button>-->

        <!--        <button-->
        <!--          class="flex mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md justify-between"-->
        <!--          onclick={() => showLanguageMenu = !showLanguageMenu}-->
        <!--        >-->
        <!--          <span>Language</span>-->
        <!--          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">-->
        <!--            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>-->
        <!--          </svg>-->
        <!--        </button>-->

        <!--        {#if showLanguageMenu}-->
        <!--          <div class="absolute left-full top-0">-->
        <!--            <ul class="menu gap-1 bg-base-100 rounded-lg min-w-48 p-2 shadow-lg border border-gray-200">-->
        <!--              {#each languages as lang}-->
        <!--                <li>-->
        <!--                  <button-->
        <!--                    class="flex gap-3 items-center text-sm hover:bg-gray-100 rounded-md px-3 py-2 {currentLanguage === lang.code ? 'bg-gray-100' : ''}"-->
        <!--                    onclick={() => selectLanguage(lang.code)}-->
        <!--                  >-->
        <!--                    <span class="text-lg">{lang.flag}</span>-->
        <!--                    <span>{lang.name}</span>-->
        <!--                    {#if currentLanguage === lang.code}-->
        <!--                      <svg class="w-4 h-4 ml-auto text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">-->
        <!--                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>-->
        <!--                      </svg>-->
        <!--                    {/if}-->
        <!--                  </button>-->
        <!--                </li>-->
        <!--              {/each}-->
        <!--            </ul>-->
        <!--          </div>-->
        <!--        {/if}-->

      </li>

      <div class="dropdown dropdown-left">
        <button tabindex="0" class="flex w-full mx-2 p-1 gap-2 items-center text-sm hover:bg-gray-100 rounded-md"
                onclick={() => showLanguageMenu = !showLanguageMenu}
        >
          Lang
        </button>
        {#if showLanguageMenu}
          <ul class="menu dropdown-content bg-base-100 rounded-lg z-[1] w-52 p-2 shadow">
            {#each languages as lang}
              <li>
                <button>
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
