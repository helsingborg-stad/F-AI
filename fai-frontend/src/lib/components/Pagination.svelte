<script lang="ts" context="module">
    const createPaginateUrl = (path: string, query_var: string, page: number) => {
        let params = new URLSearchParams(window.location.search);
        params.set(query_var, page.toString());
        return `${path}?${params.toString()}`;
    }

    const buildPaginationLinks = (path: string, current: number, total: number, limit: number, query_var: string): {
        page: number | string,
        url?: string,
        text: string
    }[] => {
        const links = [];


        // Determine the start and end page numbers for the pagination links
        let start_page = Math.max(current - Math.floor(limit / 2), 1);
        console.log(start_page)
        let end_page = start_page + limit - 1;

        if (end_page > total) {
            end_page = total;
            start_page = Math.max(1, end_page - limit + 1);
        }

        // Add the first page and "..." if necessary
        if (start_page > 1) {
            links.push({
                page: 1,
                url: createPaginateUrl(path, query_var, 1),
                text: '1'
            });

            links.push({
                page: '...',
                text: '...'
            });

        }

        // Generate the visible range of pagination links
        for (let page = start_page; page <= end_page; page++) {
            links.push({
                page: page,
                url: createPaginateUrl(path, query_var, page),
                text: page.toString()
            });
        }

        // Add "..." and the last page if necessary
        if (end_page < total) {
            links.push({
                page: '...',
                text: '...'
            });

            links.push({
                page: total,
                url: createPaginateUrl(path, query_var, total),
                text: total.toString()
            });
        }

        return links;
    }
</script>

<script lang="ts">
    import {path} from 'elegua';
    import Link from "./Link.svelte";

    export let current: number
    export let total: number
    export let limit: number = 5
    export let query_var: string = 'page'

    let links: {
        page: number | string,
        url?: string,
        text: string
    }[] = []

    $: {
        links = buildPaginationLinks($path, current, total, limit, query_var)
    }
</script>

<div class="join">
    {#each links as link}
        {#if link.url}
            {#if link.page === current}
                <span class="join-item btn btn-outline btn-active btn-neutral btn-square btn-sm  pointer-events-none">{link.text}</span>
            {:else}
                <Link class="join-item btn btn-outline btn-square btn-sm" href={link.url}>{link.text}</Link>
            {/if}
        {:else}
            <span class="btn join-item   btn-outline btn-square disabled btn-neutral hover:bg-transparent pointer-events-none hover:text-current btn-sm">{link.text}</span>
        {/if}
    {/each}
</div>
