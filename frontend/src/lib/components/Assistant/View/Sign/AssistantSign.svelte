<script lang="ts">
  import { goto } from '$app/navigation'
  import FavCheckbox from '$lib/components/Assistant/View/Sign/FavCheckbox.svelte'
  import ShareButton from '$lib/components/Assistant/View/Sign/ShareButton.svelte'
  import Avatar from '$lib/components/Assistant/View/Sign/Avatar.svelte'

  interface Props {
    id: string
    avatar: string
    avatarThumbnail?: string | null
    primaryColor?: string
    title: string
    owner: string
    description: string
    starters: string[]
    isFavorite: boolean
    getAssistantAvatar?: (assistantId: string) => Promise<string>
    metadata: {
      category: string
      conversationCount: string
      likes: string
    }
  }

  let { 
    id, 
    avatar, 
    avatarThumbnail, 
    primaryColor = '#6366f1', 
    title, 
    owner, 
    description, 
    starters, 
    isFavorite, 
    getAssistantAvatar,
    metadata 
  }: Props = $props()

  function chatWithAssistant() {
    goto(`/chat/?assistant_id=${id}`)
  }
</script>

<div class="grow overflow-y-auto">
  <div class="flex h-full px-2 py-4">
    <div class="relative flex grow flex-col gap-4 overflow-y-auto px-8 pt-16 pb-20">
      <div class="absolute top-0">
        <div class="fixed end-4 z-10 flex items-center justify-center gap-1">
          <ShareButton link={`/assistant/zoo?id=${id}`} />
          <FavCheckbox {id} {isFavorite} />
        </div>
      </div>

      <div class="absolute bottom-[64px]">
        <div class="fixed start-4 end-4 z-10 flex items-end px-2">
          <button class="btn btn-neutral w-full" onclick={() => {chatWithAssistant()}}>
            Chat with assistant
          </button>
        </div>
      </div>

      <div class="flex h-full flex-col items-center">
        <div class="avatar relative mb-3">
          <div class="rounded">
            {#if getAssistantAvatar}
              <Avatar
                {id}
                {avatar}
                {avatarThumbnail}
                {title}
                {primaryColor}
                {getAssistantAvatar}
                class="block max-w-32 max-h-47 w-auto h-auto"
              />
            {:else}
              <img
                src={avatar}
                alt="avatar"
                class="block max-w-32 max-h-47 w-auto h-auto"
              />
            {/if}
          </div>
        </div>
        <div class="flex flex-col items-center gap-2">
          <div class="text-center text-2xl font-semibold">
            {title}
          </div>
          <div class="text-center text-sm text-gray-400">
            {#if owner}
              By {owner}
            {/if}
          </div>
          <div class="text-center max-w-md text-sm font-normal">
            {description}
          </div>
        </div>
      </div>

      <!--      Stats-->
      <div class="flex justify-center">
        <div class="stats shadow">
          <div class="stat">
            <div class="stat-title">Category</div>
            <div class="stat-value">{metadata.category}</div>
          </div>
          <div class="stat">
            <div class="stat-title">Conversations</div>
            <div class="stat-value">{metadata.conversationCount}</div>
          </div>
          <div class="stat">
            <div class="stat-title">Total Likes</div>
            <div class="stat-value">{metadata.likes}</div>
          </div>
        </div>
      </div>

      <!--      Conversation starters-->
      {#if starters}
        <div class="flex flex-col">
          <div class="font-bold mt-6">
            Conversation starters
          </div>
          <div class="mt-4 grid grid-cols-2 grid-x-1.5 gap-y-2">
            {#each starters as starter}
              <div class="chat chat-end">
                <div class="chat-bubble">
                  {starter}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!--      Ratings-->
      <div class="flex flex-col">
        <div class="mb-2">
          <div class="font-bold mt-6">Ratings</div>
        </div>
        <div class="text-sm text-gray-400">Not enough ratings yet</div>
      </div>

    </div>
  </div>
</div>
