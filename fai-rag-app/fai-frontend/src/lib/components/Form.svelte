<script lang="ts">
    import type {IRenderableComponent} from "../types";
    import {createForm} from 'felte';
    import {pageDataStore} from "../store";
    import {writable} from "svelte/store";

    const responseToFormErrorAdapter = (error: any) => ({
        path: (error?.loc || [null, 'this'])[1],
        message: error?.msg || error.body || 'An error occurred',
    });


    const shouldReceiveFormProps = ({type, props}: IRenderableComponent) => true

    export let components: IRenderableComponent[] = [];
    let fields = writable<IRenderableComponent[]>([])


    let {form, errors, touched, isSubmitting, interacted, setTouched, isDirty} = createForm({
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

    $: {
        components && $errors && $isSubmitting && $interacted
        $fields = components.map((component) => (
            {
                ...component,
                props: {
                    ...component.props,
                    error: $isDirty && !$interacted ? $errors[component.props.name] : !$isDirty && $interacted ? $errors[component.props.name] : undefined,
                }
            }
        ))
    }


    export let className: string | undefined = ""
    export {className as class}
    export let action: string | undefined
    export let method: "post" | "get" | undefined
    export let footer: IRenderableComponent[] | undefined = undefined;
    export let submit_text: string = "Submit";
    export let id: string = action || "form" + method || "post";
    const attributes = writable({})
    $: {
        $attributes = {
            ...$attributes,
            id,
            action,
            method,
            "class": ["form", "space-y-6", "group", className].filter(c => c).join(" "),
        }
    }


</script>

{#key $$props}
    <form use:form class:has-interacted={$interacted} class:is-dirty={$isDirty} class:is-submitting={$isSubmitting}
          {...$attributes}>
        <slot name="fields">
            {#each $fields as {type, props}}
                <svelte:component this={type} {...props}/>
            {/each}
        </slot>

        <slot name="footer">
            {#if footer}
                {#each footer as component}
                    {#key component}
                        <svelte:component this={component.type} {...component.props}/>
                    {/key}
                {/each}
            {:else}
                <button class="btn btn-neutral btn-block" type="submit">{submit_text}</button>
            {/if}

            {#if $errors['this']}
                <div class="label-text text-error text-center">
                    {$errors['this']}
                </div>
            {/if}
        </slot>
    </form>
{/key}