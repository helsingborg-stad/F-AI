<script lang="ts">
    import type {IRenderableComponent} from "../types"
    import {createForm} from 'felte'
    import {pageDataStore} from "../store"
    import {writable} from "svelte/store"

    const responseToFormErrorAdapter = (error: any) => ({
        path: (error?.loc || [null, 'this'])[1],
        message: error?.msg || error.body || 'An error occurred',
    })

    export let components: IRenderableComponent[] = []
    let fields = writable<IRenderableComponent[]>([])

    let {form, errors, touched, isSubmitting, interacted, setTouched, isDirty, data} = createForm({
        onSubmit(values, context) {
            return fetch(action || "", {
                method: method || "post",
                body: JSON.stringify(values),
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(async r => {
                if (!r.ok) {
                    throw await r.json();
                }
                return r.json();
            })
        },
        onError: async (errors: any, context) => {
            return (context.setTouched({}) == null) && [...(errors?.detail || [])]
                .reduce((acc: any, error: any) => {
                    const {path, message} = responseToFormErrorAdapter(error)
                    return {
                        ...acc,
                        [path]: message,
                    }
                }, {})
        },
        onSuccess: async (response: any, context) => {
            const components_response = [...[...(response || [])].filter((item) => item.type)]
            if (components_response.length > 0) {
                $pageDataStore = components_response
            }
        },
    })

    $: console.log($data)

    $: {
        components && $errors && $isSubmitting && $interacted
        $fields = components.map((component) => (
            {
                ...component,
                props: {
                    ...component.props,
                    error: $isDirty && !$interacted ? $errors[component.props.name] : !$isDirty && $interacted ? $errors[component.props.name] : null,
                }
            }
        ))
    }

    export let className: string | null = ""
    export {className as class}
    export let action: string | null
    export let method: "post" | "get" | null
    export let submit_text: string | null = null
    export let id: string = action || "form" + method || "post"
    const attributes = writable({})
</script>

{#key $$props}
    <form
            {id}
            {action}
            {method}
            use:form
            class:has-interacted={$interacted}
            class:is-dirty={$isDirty}
            class:is-submitting={$isSubmitting}
            class:form={true}
            class:group={true}
            class:space-y-6={true}
            {...$attributes}>
        <slot name="fields">
            {#each $fields as {type, props}}
                <svelte:component this={type} {...props}/>
            {/each}
        </slot>

        <slot name="footer">
            {#if submit_text}
                <button class="btn btn-neutral" type="submit">{submit_text}</button>
            {/if}

            {#if $errors['this']}
                <div class="label-text text-error text-center">
                    {$errors['this']}
                </div>
            {/if}
        </slot>
    </form>
{/key}