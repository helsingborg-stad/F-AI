<script lang="ts">

    export let hasDrawer: boolean | null = null;
</script>

<div class:drawer={$$slots?.drawer || hasDrawer} class:lg:drawer-open={$$slots?.drawer || hasDrawer}>
    {#if $$slots?.drawer || hasDrawer}
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle"/>
        <slot name="drawer"/>
    {/if}

    <slot/>
</div>
