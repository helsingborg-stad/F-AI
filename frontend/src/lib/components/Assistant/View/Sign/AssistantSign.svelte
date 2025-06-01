<script lang="ts">
  import { goto } from '$app/navigation'

  interface Props {
    id: string
    avatar: string
    title: string
    owner: string
    description: string
    category: string
    conversationCount: number
    starters: string[]
  }

  let { id, avatar, title, owner, description, category, conversationCount, starters }: Props = $props()

  function chatWithAssistant() {
    goto(`/chat/?assistant_id=${id}`)
  }
</script>

<div class="grow overflow-y-auto">
  <div class="flex h-full px-2 py-4">
    <div class="relative flex grow flex-col gap-4 overflow-y-auto px-8 pt-16 pb-20">

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
            <img
              src={avatar}
              alt="avatar"
              class="block"
              style="max-width: 128px; max-height: 188px; width: auto; height: auto;"
            />
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
            <div class="stat-value">{category}</div>
          </div>
          <div class="stat">
            <div class="stat-title">Conversations</div>
            <div class="stat-value">{conversationCount}</div>
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
