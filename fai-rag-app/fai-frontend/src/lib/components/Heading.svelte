<!-- Heading.svelte -->
<script lang="ts">
    import Text from "./Text.svelte"

    export let level: number = 1 // Default to h1
    export let text: string = ''

    let className: string | null = null
    export {className as class}

    // Determine the heading type dynamically based on the level prop
    $: Tag = `h${Math.min(6, Math.max(1, level))}` as keyof HTMLElementTagNameMap
</script>

<Text element={Tag} {...$$props}>
    <slot>{text}</slot>
</Text>
