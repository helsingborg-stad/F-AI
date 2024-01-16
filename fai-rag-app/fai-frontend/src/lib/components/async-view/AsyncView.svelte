<script lang="ts">
    import createAsyncStore, {type AsyncState} from "./async-store";

    type TData = $$Generic
    type TState = $$Generic
    export let promise: Promise<TData>
    export let initialState: TState
    export let initialData: TData

    const initial = {
        promise,
        data: initialData,
        state: initialState
    }

    const {subscribe, update} = createAsyncStore<TData, TState>(initial.data, initial.state)

    update(initial.state, () => initial.promise)

    let state: AsyncState<TData, TState>
    
    subscribe((value: AsyncState<TData, TState>) => {
        state = value;
    });

    const updateState: (state: TState, callback: () => Promise<TData>) => any = update
</script>

{#if state.isPending}
    <slot name="pending" state={state.state} data={state.data} error={state.error} {updateState}>{updateState}</slot>
{:else if state.error === null}
    <slot name="resolved" state={state.state} data={state.data} error={state.error} {updateState}>{updateState}</slot>
{:else if state.error}
    <slot name="rejected" state={state.state} data={state.data} error={state.error} {updateState}>{updateState}</slot>
{/if}


<script lang="ts" context="module">
    export type Props<TData, TState> = {
        promise: Promise<TData>
        initialState: TState
        initialData: TData
    }
</script>

