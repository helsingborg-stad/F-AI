<script lang="ts">
    import Link from "./Link.svelte";

    let className: string | null = null
    export {className as class}

    export let columns: {
        key: string
        label: string
        link_text?: string
    }[] = []
    export let data: { [key: string]: any }[] = []
    export let headerClass: string = ''
    export let rowClass: string = ''
    export let cellClass: string = ''
</script>

{#if columns.length > 0}
    <table class:table={true} class:border={false} class={className}>
        <thead>
        <tr class={headerClass}>
            {#each columns as column}
                <th class={cellClass}>
                    <slot name="header" column={column}>{column.label}</slot>
                </th>
            {/each}
        </tr>
        </thead>

        <tbody>
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
        </tbody>
    </table>
{/if}

{#if columns.length === 0}
    <slot name="cell" data={data} columns={columns}>
        <span class="text-error">No columns defined in table</span>
    </slot>
{/if}
