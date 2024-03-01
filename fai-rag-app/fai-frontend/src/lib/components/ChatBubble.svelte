<script lang="ts">
    import SvelteMarkdown from "svelte-markdown";

    import Text from "./Text.svelte";

    export let imageSrc: string | null = null
    export let user: string | null = null
    export let time: string | null = null
    export let isSelf: boolean | null = null
    export let content: string | null = null


</script>

<div class:w-full={1} class:max-w-prose={1} class:mx-auto={1} class:chat-start={1} class:chat={1} class:p-4={1}
     class:py-6={1}
     {...$$restProps}>

    <div class="chat-header">
        <Text class="text-xs font-bold">{user}</Text>
        <time class="text-xs opacity-50">{time}</time>
        <slot name="header"/>
    </div>

    <div class:bg-primary={isSelf}
         class="chat-bubble bg-transparent text-base-content px-0 prose">
        <SvelteMarkdown source={content}/>
        <slot name="below-content"/>
    </div>

    {#if $$slots.footer}
        <div class="chat-footer">
            <slot name="footer"/>
        </div>
    {/if}

</div>
