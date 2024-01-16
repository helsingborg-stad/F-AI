<!-- Heading.svelte -->
<script lang="ts">
    export let level: number = 1; // Default to h1
    export let text: string = '';

    let className: string | undefined

    export {className as class}

    const props = {
        ...className ? {class: className} : {},
    }
    // Determine the heading type dynamically based on the level prop
    $: Tag = `h${Math.min(6, Math.max(1, level))}` as keyof HTMLElementTagNameMap;
</script>

<svelte:element this={Tag} {...props}>
    <slot>{text}</slot>
</svelte:element>
