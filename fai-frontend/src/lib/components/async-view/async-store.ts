import {writable} from 'svelte/store';

export type AsyncState<TData, TState> = {
    state: TState;
    data: TData;
    error: Error | null;
    isPending: boolean;
}

export function createAsyncStore<TData, TState>(initialData: TData, initialState: TState) {
    const {subscribe, update, set} = writable<AsyncState<TData, TState>>({
            state: initialState,
            data: initialData,
            error: null,
            isPending: true
        }
    );

    const setState = async (state: TState, callback: () => Promise<TData>): Promise<void> => {
        update(asyncState => ({...asyncState, state, error: null, isPending: true}))
        try {
            const newData = await callback();
            update(asyncState => ({...asyncState, data: newData, error: null, isPending: false}));
        } catch (error: any) {
            update(asyncState => ({...asyncState, error, isPending: false}));
        }
    };

    return {
        subscribe,
        update: setState,
    }
}

export default createAsyncStore;
