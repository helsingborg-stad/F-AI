<script lang="ts">
    export let text: string | null = null;
    export let altText: string | null = null;
</script>

<span class="label" {...$$restProps}>
    {#if text !== null || $$slots.default}
        <span class="label-text">
           <slot>{text}</slot>
        </span>
    {/if}
    {#if altText !== null || $$slots.altText}
    <span class="label-text-alt">
        <slot name="altText">{altText}</slot>
    </span>
    {/if}
</span>