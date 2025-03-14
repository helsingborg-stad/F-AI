<script lang="ts">
	export let icon: string = '';
  export let width: number = 24;
  export let height: number = 24;

    $: finalIcon = icon
    ? icon
        .replace(/width="24"/, `width="${width}"`)
        .replace(/height="24"/, `height="${height}"`)
    : '';
</script>

{#if finalIcon}
  <span>{@html finalIcon}</span>
{/if}