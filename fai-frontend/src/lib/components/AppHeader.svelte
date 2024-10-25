<script lang="ts">
    import {type IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = []
</script>

<nav class="navbar tracking-tight top-0 sticky w-full bg-opacity-40 bg-base-100 backdrop-blur px-0 border-neutral border-opacity-25 border-b z-50">
    <div class="px-4 w-full">
        <div class="flex-1 lg:flex-none lg:hidden">
            <label for="my-drawer-2" aria-label="open sidebar" class="btn btn-square btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                     class="inline-block w-6 h-6 stroke-current">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            </label>
        </div>
        <slot>
            {#each components as component}
                <svelte:component this={component.type} {...component.props}/>
            {/each}
        </slot>
    </div>
</nav>