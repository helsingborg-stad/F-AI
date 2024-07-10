<script lang="ts">
    import type {Readable, Writable} from "svelte/store";
    import type {DisplayColumnDef} from "$lib/components/table/types";
    import {getDistinct, normalizeFlatten, normalizeToArray} from "$lib/components/table/array";
    import {type BodyRow} from "svelte-headless-table";
    import MultiSelect from "$lib/components/MultiSelect.svelte";
    import {FormControl, Label} from "$lib/components/input";
    import SVG from "$lib/components/SVG.svelte";
    import Button from "$lib/components/Button.svelte";

    type T = $$Generic

    export let id: string | null
    export let filterValue: Writable<any>
    export let values: Readable<any[]>
    export let preFilteredValues: Readable<any[]>
    export let preFilteredRows: Readable<BodyRow<T>[]>
    export let initialFilterValue: any
    export let column: DisplayColumnDef

    export const resetHandler = () => {
        $filterValue = []
    }

    const mapOptions = (options: [string, string][]): [string, string, boolean | null][] => options.map(
        ([value, label]) => ({
            value,
            label,
        }))
        .map(({value, label}) => [value, label, null])

    $: options = mapOptions(column?.filterOptions ?? getDistinct(normalizeFlatten($preFilteredValues)).map(v => [v, v]))
    $: value = normalizeToArray((initialFilterValue || $filterValue) ?? [])
    $: showReset = value.length > 0

    $: (console.log(id))

</script>
<div class:badge-outline={showReset} class="border px-4 pb-4">
    <FormControl name={id ?? column.id ?? column.key} label={column.label} size="sm">
        <svelte:fragment slot="label">
            <Label>
                <span class:text-xs={1} class:font-semibold={1}>{column.label}</span>
                <svelte:fragment slot="altText">
                    {#key showReset}
                        <div class="join">


                            <Button
                                    html_type="reset"
                                    slot="after"
                                    size="xs"
                                    circle

                                    class={[
                                    !showReset ? "opacity-0" : null,
                                    'join-item',
                                ].filter(v => v && v?.length && v.trim().length > 0).join(' ')}
                                    disabled={!showReset}
                                    on:click={resetHandler}
                            >
                                <SVG
                                        class="inline-block h-4 w-4"
                                        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXgiPjxwYXRoIGQ9Ik0xOCA2IDYgMTgiLz48cGF0aCBkPSJtNiA2IDEyIDEyIi8+PC9zdmc+"/>
                            </Button>
                        </div>
                    {/key}
                </svelte:fragment>
            </Label>
        </svelte:fragment>

        <svelte:fragment>
            {#key showReset}
                <MultiSelect
                        class="select-sm"
                        name={id ?? column.id ?? column.key}
                        {value}
                        {options}
                        on:inputChange={(e) => $filterValue !== e.detail ? $filterValue = e.detail : null}
                />

            {/key}
        </svelte:fragment>
    </FormControl>
</div>