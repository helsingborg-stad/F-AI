<script lang="ts">
    import type {IRenderableComponent} from "../types";
    import {createForm} from 'felte';
    import {pageDataStore} from "../store";


    const responseToFormErrorAdapter = (error: any) => ({
        path: error.loc[1],
        message: error.msg
    });

    let {form, errors, touched, isSubmitting, createSubmitHandler, setTouched, isDirty} = createForm({
        onError: async (errors: any, context) =>
            (context.setTouched({}) == null) && [...(await errors.response.json())?.detail || []]
                .reduce((acc: any, error: any) => {
                    const {path, message} = responseToFormErrorAdapter(error);
                    return {
                        ...acc,
                        [path]: message,
                    };
                }, {}),
        onSuccess: async (response: any, context) => {
            console.log(response)
            const items = [...(response?.detail || await response?.json() || [])]
            console.log([...items.filter((item) => item.type === 'FireEvent')])

            const events = [...items.filter((item) => item.type === 'FireEvent')]
            if (events.length > 0) {
                $pageDataStore = events
            }
        },
    });

    let className: string | undefined

    export {className as class}
    export let action: string | undefined
    export let method: "post" | "get" | undefined
    export let components: IRenderableComponent[] = [];
    export let footer: IRenderableComponent[] | undefined = undefined;
    export let submit_text: string = "Submit";

    const props = {
        ...className ? {class: className} : {
            class: "form space-y-6"
        },
        ...action ? {action} : {},
        ...method ? {method} : {}
    }
</script>

<form use:form {...props}>
    <slot name="fields">
        {#each components as component}
            <svelte:component this={component.type} {...component.props}/>
        {/each}
    </slot>

    <slot name="footer">
        {#if footer}
            {#each footer as component}
                <svelte:component this={component.type} {...component.props}/>
            {/each}
        {:else}
            <button class="btn btn-neutral btn-block" type="submit">{submit_text}</button>
        {/if}
    </slot>
</form>
