<script lang="ts">
    import Select from "$lib/components/Select.svelte";
    import type {Readable, Writable} from "svelte/store";
    import type {DisplayColumnDef} from "$lib/components/table/types";
    import {getDistinct} from "$lib/components/table/array";
    import {type BodyRow} from "svelte-headless-table";

    type T = $$Generic

    export let id: string
    export let filterValue: Writable<any>
    export let values: Readable<any[]>
    export let preFilteredValues: Readable<any[]>
    export let preFilteredRows: Readable<BodyRow<T>[]>
    export let initialFilterValue: any
    export let column: DisplayColumnDef

    const mapOptions = (options: [string, string][]): [string, string, boolean | null][] => options.map(
        ([value, label]) => ({
            value,
            label,
        }))
        .map(({value, label}) => [value, label, null])

    $: options = mapOptions(column?.filterOptions ?? getDistinct($preFilteredValues).map(v => [v, v]))
    $: value = (initialFilterValue || $filterValue) ?? ''

</script>


<Select class="select-xs" name={id} {value} on:input={(e) => $filterValue = e?.target?.value} {options}/>