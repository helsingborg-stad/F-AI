<script lang="ts">
    export let columns: { key: string; title: string }[] = [];
    export let data: { [key: string]: any }[] = [];
    export let tableClass: string = 'table'; // default class
    export let headerClass: string = '';
    export let rowClass: string = '';
    export let cellClass: string = '';
</script>

{#if columns.length > 0}
    <table class={tableClass}>
        <thead>
        <tr class={headerClass}>
            {#each columns as column}
                <th>
                    <slot name="header" column={column}>{column.title}</slot>
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
                            {rowData[column.key]}
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
