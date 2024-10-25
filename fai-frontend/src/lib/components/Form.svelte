<script lang="ts">
  import type { IComponentDef, IRenderableComponent } from '../types'
  import { createForm } from 'felte'
  import { writable } from 'svelte/store'
  import { pageDataStore } from '../store'
  import Button from './Button.svelte'

  export let components: IRenderableComponent[] = []
  let fields = writable<IRenderableComponent[]>([])

  export let submitAs: 'json' | 'form' = 'json'

  const tryRenderComponentsFromResponse = (components: IComponentDef[]) => {
    const components_response = [...[...(components || [])].filter((item) => item.type)]
    if (components_response.length > 0) {
      $pageDataStore = components_response
    }
  }

  const tryMapErrorResponseToFormFields = (error: any) => ({
    path: (error?.loc || [null, 'this'])[1],
    message: error?.msg || error.body || 'An error occurred',
  })

  const parseErrorResponseObjects = (errors: object[] = []) =>
    [...errors].reduce((acc: any, error: any) => {
      const { path, message } = tryMapErrorResponseToFormFields(error)
      return {
        ...acc,
        [path]: message,
      }
    }, {})

  const formHandlerFactory = (
    submitType: 'json' | 'form',
  ): {
    createFormConfiguration: any
    successHandler: any
    errorHandler: any
  } => ({
    createFormConfiguration: {
      json: () => ({
        onSubmit: (values: any, context: any) =>
          fetch(action || '', {
            method: method || 'post',
            body: JSON.stringify(values),
            headers: {
              'Content-Type': 'application/json',
            },
          }).then(async (r) => {
            if (!r.ok) {
              throw r
            }
            return r.json()
          }),
        onError: async (response: any, context: any) => {
          const isJson = response.headers.get('content-type').includes('application/json')
          const fieldErrors = (isJson ? await response.json() : null)?.detail || []
          return parseErrorResponseObjects(fieldErrors)
        },
        onSuccess: async (response: any, context: any) => {
          const components_response = [
            ...[...(response || [])].filter((item) => item.type),
          ]
          if (components_response.length > 0) {
            $pageDataStore = components_response
          }
        },
      }),

      form: () => ({}),
    }[submitType],
    successHandler: {
      json: undefined,
      form: async (e: CustomEvent<any>) => {
        const isJson = e.detail.response.headers
          .get('content-type')
          .includes('application/json')
        isJson && tryRenderComponentsFromResponse(await e.detail.response.json())
      },
    }[submitType],
    errorHandler: {
      json: undefined,
      form: async ({
        detail: {
          error: { response },
        },
      }: CustomEvent<any>) => {
        const { detail } = response.headers
          .get('content-type')
          .includes('application/json')
          ? await response.json()
          : { detail: [] }

        return parseErrorResponseObjects(detail || [])
      },
    }[submitType],
  })

  const { createFormConfiguration, successHandler, errorHandler } =
    formHandlerFactory(submitAs)

  let { form, errors, touched, isSubmitting, interacted, setTouched, isDirty, data } =
    createForm({
      ...createFormConfiguration(),
    })

  $: {
    components && $errors && $isSubmitting && $interacted
    $fields = components.map((component) => ({
      ...component,
      props: {
        ...component.props,
        error:
          $isDirty && !$interacted
            ? $errors[component.props.name]
            : !$isDirty && $interacted
              ? $errors[component.props.name]
              : null,
      },
    }))
  }

  export let className: string | null = ''
  export { className as class }
  export let action: string | null
  export let method: 'post' | 'get' | 'patch' | null
  export let submit_text: string | null = null
  export let id: string = action || 'form' + method || 'post'
  const attributes = writable({})
</script>

{#key $$props}
  <form
    {id}
    {action}
    {method}
    use:form
    on:felteerror={errorHandler}
    on:feltesuccess={successHandler}
    class:has-interacted={$interacted}
    class:is-dirty={$isDirty}
    class:is-submitting={$isSubmitting}
    class:form={true}
    class:group={true}
    class:space-y-6={true}
    {...$attributes}
  >
    <slot name="fields">
      {#each $fields as { type, props }}
        <svelte:component this={type} {...props} />
      {/each}
    </slot>

    <slot name="footer">
      {#if submit_text}
        <Button html_type="submit" state="neutral">{submit_text}</Button>
      {/if}

      {#if $errors['this']}
        <div class="label-text text-center text-error">
          {$errors['this']}
        </div>
      {/if}
    </slot>
  </form>
{/key}
