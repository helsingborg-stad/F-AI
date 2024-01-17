<script lang="ts">
    export let title: string = 'folketsAI'
    export let links: {
        url: string,
        name: string
    }[] = []

    import type {IRenderableComponent} from "../types";

    export let components: IRenderableComponent[] = [];
</script>

<div class="drawer lg:drawer-open">
    {#if links.length > 0}
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle"/>
        <div class="drawer-side z-10">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
            <aside class="bg-base-200 min-h-screen w-80">
                <div class="bg-base-200 sticky top-0 z-20 flex items-center px-4 py-2">
                    <a href="/" class="flex-0 btn btn-ghost px-2 btn-lg font-extrabold text-2xl">{title}</a>
                </div>
                <ul class="menu px-4 py-2">
                    {#each links as link}
                        <li>
                            <a href={link.url}>{link.name}</a>
                        </li>
                    {/each}
                </ul>
            </aside>
        </div>
    {/if}
    <div class="drawer-content flex flex-col">
        {#if links.length > 0}
            <nav class="navbar fixed bg-opacity-60 bg-base-100 backdrop-blur px-0">
                <div class="px-2 w-full">
                    <div class="flex-1">
                        <a class="btn btn-ghost btm-nav-sm text-xl lg:hidden">{title}</a>
                    </div>
                    <div class="flex-none">
                        <label for="my-drawer-2" class="btn btn-square btn-ghost drawer-button lg:hidden">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                 class="inline-block w-5 h-5 stroke-current">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                      d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </label>
                    </div>
                </div>
            </nav>
        {/if}
        <div class="mt-16">
            <slot>
                {#each components as component}
                    <svelte:component this={component.type} {...component.props}/>
                {/each}
            </slot>
        </div>
    </div>
</div>