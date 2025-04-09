<script lang="ts">
  import Login from '$lib/components/Login/Login.svelte'
  import { setUser } from '$lib/state/user.svelte.js'

  let { form } = $props()

  const id = form?.email ? String(form.email) : ''
  setUser({ email: id })

  const isIdSubmitted = form?.isIdSubmitted ? form?.isIdSubmitted : false
  const errorMessage = form?.error ? form.error : ''
  const requestId = form?.request_id ? form.request_id : ''
</script>

<div class="min-h-screen bg-base-200 flex items-center justify-center p-4">
  <Login
    initialId={id}
    initialIsIdSubmitted={isIdSubmitted}
    errorMessage={errorMessage}
    requestId={requestId}
  />
</div>
