<script lang="ts">
    import type {IRenderableComponent} from "../types"
    import Container from "./Container.svelte";
    import Card from "./Card.svelte";

    export let title: string = 'folketsAI'
    export let links: {
        url: string,
        name: string
    }[] = []

    export let components: IRenderableComponent[] = [];
</script>

<div class="drawer lg:drawer-open">
    {#if links.length > 0}
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle"/>
        <div class="drawer-side ">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
            <div class="w-80 h-screen"></div>
            <aside class="bg-base-100 min-h-screen w-80 fixed z-50 left-0 top-0 z-50 border-r border-neutral shadow">
                <div class="sticky top-0 z-20 flex items-center px-4 py-2">
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
            <nav class="navbar fixed w-full lg:w-[calc(100%-20rem)] bg-opacity-60 bg-base-100 backdrop-blur px-0 z-10 shadow border-b border-neutral">
                <div class="px-6 w-full">

                    <div class="flex-none">
                        <label for="my-drawer-2" class="btn btn-square btn-ghost drawer-button lg:hidden">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                 class="inline-block w-5 h-5 stroke-current">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                      d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </label>
                    </div>
                    <div class="flex-1">
                        <div class="text-xl breadcrumbs">
                            <ul>
                                <li>
                                    <h1 class="font-semibold">Mina Konversationer</h1>
                                </li>
                            </ul>
                        </div>

                    </div>

                    <div class="flex-1 text-right"><label for="my-drawer-2" class="btn btn-square btn-ghost">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                             stroke-linejoin="round" class="lucide lucide-user-round-cog">
                            <path d="M2 21a8 8 0 0 1 10.434-7.62"/>
                            <circle cx="10" cy="8" r="5"/>
                            <circle cx="18" cy="18" r="3"/>
                            <path d="m19.5 14.3-.4.9"/>
                            <path d="m16.9 20.8-.4.9"/>
                            <path d="m21.7 19.5-.9-.4"/>
                            <path d="m15.2 16.9-.9-.4"/>
                            <path d="m21.7 16.5-.9.4"/>
                            <path d="m15.2 19.1-.9.4"/>
                            <path d="m19.5 21.7-.4-.9"/>
                            <path d="m16.9 15.2-.4-.9"/>
                        </svg>
                    </label></div>
                </div>
            </nav>
        {/if}
        <div class="mt-20">
            <Container>


                <Card
                        title="Shoes!"
                        description="If a dog chews shoes whose shoes does he choose?"
                        imageSrc="/images/stock/photo-1606107557195-0e29a4b5b4aa.jpg"
                        imageAlt="Shoes"
                        actionText="Buy Now"
                        badge="New"
                        badgeStyle="bg-accent text-accent-content"
                />

            </Container>
            <slot>
                {#each components as component}
                    <svelte:component this={component.type} {...component.props}/>
                {/each}
            </slot>
        </div>
    </div>
</div>