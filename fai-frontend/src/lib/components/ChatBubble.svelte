<script lang="ts">
  import SvelteMarkdownWrapper from "$lib/components/SvelteMarkdownWrapper.svelte";

  import Text from './Text.svelte'

  export let imageSrc: string | null = null
  export let user: string | null = null
  export let time: string | null = null
  export let isSelf: boolean | null = null
  export let content: string | null = null

  export let enableMarkdown: boolean = false
</script>

<div
  class:w-full={1}
  class:max-w-prose={1}
  class:mx-auto={1}
  class:chat-start={!isSelf}
  class:chat-end={isSelf}
  class:chat={1}
  class:p-4={1}
  {...$$restProps}
>
  <div class="chat-header">
    {#if user}
      <Text class="text-xs font-bold">{user}</Text>
    {/if}
    {#if time}
      <time class="text-xs opacity-50">{time}</time>
    {/if}
    <slot name="header"/>
  </div>

  <div
    class:bg-base-200={isSelf}
    class:bg-transparent={!isSelf}
    class:before:bg-transparent={!isSelf}
    class:p-0={!isSelf}
    class="prose chat-bubble min-h-fit text-base-content"
  >
    {#if enableMarkdown}
      <SvelteMarkdownWrapper source={content}/>
    {:else}
      <span class="whitespace-pre-line">{content}</span>
    {/if}
    <slot name="below-content"/>
  </div>

  {#if $$slots.footer}
    <div class="chat-footer">
      <slot name="footer"/>
    </div>
  {/if}
</div>
