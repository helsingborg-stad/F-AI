<script lang="ts">
    import Link from "./Link.svelte";
    import InlineSvgIcon from "./SVG.svelte"

    let className: string | null = null
    export {className as class}

    export let columns: {
        key: string
        label: string
        link_text?: string
        sortable?: boolean
        sort_url?: string | null
        sort_order?: 'asc' | 'desc' | null
    }[] = []
    export let data: { [key: string]: any }[] = []
    export let headerClass: string = ''
    export let rowClass: string = ''
    export let cellClass: string = ''

    const SORT_ICONS = {
        'asc': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb24tdXAiPjxwYXRoIGQ9Im0xOCAxNS02LTYtNiA2Ii8+PC9zdmc+',
        'desc': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb24tZG93biI+PHBhdGggZD0ibTYgOSA2IDYgNi02Ii8+PC9zdmc+',
        'none': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb25zLXVwLWRvd24iPjxwYXRoIGQ9Im03IDE1IDUgNSA1LTUiLz48cGF0aCBkPSJtNyA5IDUtNSA1IDUiLz48L3N2Zz4='
    }
</script>

{#if columns.length > 0}
    <table class:table={true} class:border={false} class={className}>
        <thead>
        {#key columns}
            <tr class={headerClass}>
                {#each columns as column, i}
                    <th class={cellClass}>
                        <div class:inline-flex={1}
                             class:space-x-0.5={1}
                             class:items-center={1}
                        >
                            {#key column}
                                {#if column?.sortable && column?.sort_url}

                                <span class:text-neutral={column?.sort_order}>
                                <slot name="header" column={column}>{column.label}</slot>
                            </span>
                                    <Link href={column.sort_url} size="xs"
                                          variant="ghost" square={true}>
                                        <InlineSvgIcon
                                                width="16"
                                                state={column?.sort_order ? 'neutral' : null}
                                                src={SORT_ICONS[column?.sort_order ?? 'none']}/>
                                    </Link>

                                {:else}
                                    <slot name="header" column={column}>{column.label}</slot>
                                {/if}
                            {/key}
                        </div>
                    </th>
                {/each}
            </tr>
        {/key}
        </thead>

        <tbody>
        {#key data}
            {#each data as rowData, rowIndex}
                <tr class={rowClass}>
                    {#each columns as column, colIndex}
                        <td class={cellClass}>
                            <slot name="cell" rowData={rowData} column={column} rowIndex={rowIndex} colIndex={colIndex}>
                                {#if column.link_text}
                                    <Link underline="always"
                                          href={rowData[column.key]}>{column.link_text}</Link>
                                {/if}

                                {#if !column.link_text}
                                    {rowData[column.key]}
                                {/if}
                            </slot>
                        </td>
                    {/each}
                </tr>
            {/each}
        {/key}
        </tbody>
    </table>
{/if}

{#if columns.length === 0}
    <slot name="cell" data={data} columns={columns}>
        <span class="text-error">No columns defined in table</span>
    </slot>
{/if}
