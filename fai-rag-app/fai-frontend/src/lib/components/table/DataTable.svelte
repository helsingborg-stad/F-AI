<div class="overflow-x-auto h-screen max-h-[calc(100vh-65px)] overflow-scroll">

    <ToolBar>
        <svelte:fragment slot="start">
        </svelte:fragment>
        <svelte:fragment slot="end">
            <SearchInput filterValue={$filterValue} resetHandler={() => ($filterValue = '')}
                         on:input={(e) => {$filterValue = e?.target?.value?.trim() ?? $filterValue}}/>
            {#key canResetFilterValues}
                <Button class="ml-auto join-item hidden"
                        disabled={canResetFilterValues === false}
                        on:click={resetFilters}
                >
                    <SVG
                            src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXgiPjxwYXRoIGQ9Ik0xOCA2IDYgMTgiLz48cGF0aCBkPSJtNiA2IDEyIDEyIi8+PC9zdmc+"/>
                    Reset filters
                </Button>
            {/key}
            <div class="join">
                <Button active={showFilterPanel} state={showFilterPanel ? 'neutral' : null}
                        on:click={() => (showFilterPanel = !showFilterPanel)}
                        class="ml-auto join-item"
                >
                    <SVG src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxpc3QtZmlsdGVyIj48cGF0aCBkPSJNMyA2aDE4Ii8+PHBhdGggZD0iTTcgMTJoMTAiLz48cGF0aCBkPSJNMTAgMThoNCIvPjwvc3ZnPg=="/>
                    Filters
                </Button>
            </div>
        </svelte:fragment>
    </ToolBar>
    {#key pluginStates}
        {#if showFilterPanel}
            <div class="bg-base-100  px-4 py-3 pb-8 border-b">
                <div class="indicator w-full max-w-full">
                    <span class="indicator-item indicator-end indcator -left-[calc(100%-1rem)]">
                        <Heading level={3} class="text-neutral text-md inline-block bg-base-100 px-2">
                            Filters
                        </Heading>
                    </span>
                    <div class="flex flex-col border px-4 py-8 w-full">
                        <div class="flex flex-row gap-4 items-stretch">
                            {#each $headerRows as headerRow (headerRow.id)}
                                {#each headerRow.cells as cell (cell.id)}
                                    <Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
                                        {#key props}
                                            {#key $filterValue}
                                                {#if props?.filter}
                                                    <Render of={props.filter.render}/>
                                                {/if}
                                            {/key}
                                        {/key}
                                    </Subscribe>
                                {/each}
                            {/each}
                        </div>

                        <!--  <pre>{JSON.stringify({
                         q: $filterValue,
                         filter: $filterValues,
                         sort: $sortKeys
                     }, null, 2)}</pre>-->
                    </div>
                </div>
            </div>
        {/if}
    {/key}
    {#key pluginStates}
        <table
                {...$tableAttrs}
                class:table={true}
                class:table-md={true}
                class:table-pin-rows={true}
                class:border-slate-500={1}
        >

            <thead {...$tableHeadAttrs}>
            {#each $headerRows as headerRow (headerRow.id)}
                <Subscribe rowAttrs={headerRow.attrs()} let:rowAttrs rowProps={headerRow.props()} let:rowProps>
                    <tr {...rowAttrs} {...rowProps} class:border-t-0={1}>
                        {#each headerRow.cells as cell (cell.id)}
                            <Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
                                {#key props}
                                    <th


                                            class:align-top={1}
                                            id={cell.id}
                                            {...attrs}

                                    >
                                        <div class:inline-flex={1} class:space-x-0.5={1}>
                                            <Render of={cell.render()}/>
                                            {#if !props.sort.disabled && cell.isData()}
                                                <Button
                                                        class="-mt-2 -mb-2"
                                                        variant="link"
                                                        active={['asc','desc'].includes(props.sort.order)}
                                                        on:click={props.sort.toggle} size="sm" square>
                                                    <SVG
                                                            src={SORT_ICONS[props.sort.order === 'asc' ? 'asc' : props.sort.order === 'desc' ? 'desc' : 'none']}/>
                                                </Button>
                                            {:else}
                                                <i class="w-8 h-8 -mt-2 -mb-2"></i>
                                            {/if}
                                        </div>
                                    </th>
                                {/key}
                            </Subscribe>
                        {/each}
                    </tr>
                    <tr class:hidden={1} class:static={1}>
                        {#each headerRow.cells as cell (cell.id)}
                            <Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
                                {#key props}
                                    <th class:border={1} class:border-collapse={1}>
                                        <div>
                                            {#key $filterValue}
                                                {#if props?.filter}
                                                    <Render of={props.filter.render}/>
                                                {/if}

                                            {/key}
                                        </div>
                                    </th>
                                {/key}
                            </Subscribe>
                        {/each}
                    </tr>

                </Subscribe>
            {/each}
            </thead>

            <tbody {...$tableBodyAttrs}>
            {#each $rows as row, i (row.id)}
                <Subscribe rowAttrs={row.attrs()} let:rowAttrs rowProps={{...row.props(), ...{index: i}}} let:rowProps>
                    <tr {...rowAttrs}>
                        {#each row.cells as cell (cell.id)}
                            <Subscribe attrs={cell.attrs()} let:attrs props={{...cell.props(), ...{index: i}}}
                                       let:props>
                                <td {...attrs} class:font-mono={1} class:border={1} class:border-collapse={1}>
                                    <Render of={cell.render()}/>
                                </td>
                            </Subscribe>
                        {/each}
                    </tr>
                </Subscribe>
            {/each}
            </tbody>

        </table>


    {/key}
</div>

<script lang="ts">
    import {Render, Subscribe} from "svelte-headless-table";
    import {writable} from "svelte/store";
    import SVG from "$lib/components/SVG.svelte";
    import Button from "$lib/components/Button.svelte";
    import type {DisplayColumnDef} from "$lib/components/table/types";
    import {useDataTable} from "$lib/components/table/data-table";
    import {SORT_ICONS} from "$lib/components/table/sort";
    import ToolBar from "$lib/components/table/toolbar/ToolBar.svelte";
    import SearchInput from "$lib/components/table/toolbar/SearchInput.svelte";
    import Heading from "$lib/components/Heading.svelte";


    type T = $$Generic

    export let data: T[] = []


    export let columns: DisplayColumnDef[] = []


    $: dataStore = writable<T[]>(data)
    $: $dataStore = data

    $: ({
        headerRows,
        rows,
        tableAttrs,
        tableHeadAttrs,
        tableBodyAttrs,
        visibleColumns,
        pluginStates,

        ...rest
    } = useDataTable<T>(dataStore, columns))

    $: ({

        filter: {filterValues},
        tableFilter: {filterValue},
        sort: {sortKeys}
    } = pluginStates)


    const filterIsActive = (filterValues: Record<string, string>, filterValue: string, sortKeys: string[]) => {
        return Object.values(filterValues).some((value) => value !== '') || filterValue !== '' || sortKeys.length > 0
    }

    const resetFilters = () => {
        $filterValue = ''
        $filterValues = {}
        $sortKeys = []
    }

    let canResetFilterValues: boolean = false
    $ : canResetFilterValues = filterIsActive($filterValues, $filterValue, $sortKeys)


    let showFilterPanel: boolean = false
</script>


