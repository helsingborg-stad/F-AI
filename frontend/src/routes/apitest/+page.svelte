<script lang="ts">
  import { enhance } from '$app/forms'
  import type { PageProps } from './$types'

  const { data, form }: PageProps = $props()

  $effect(() => {
    console.log('data', data)
    console.log('form', form)
  })
</script>

<div class="flex flex-col gap-4">
  <div class="flex gap-3">
    <span>Request ID: {form?.requestId}</span>
    <div class="flex flex-col gap-2">
      <span>Scopes:</span>
      {#each (form?.scopes ?? []) as scope}
        <span>{scope}</span>
      {/each}
    </div>
  </div>

  <form method="POST" action="?/loginInit" use:enhance>
    <button class="btn btn-sm" type="submit">Init Login</button>
  </form>

  <form method="POST" action="?/loginConfirm" use:enhance>
    <input type="text" class="input input-sm input-primary" name="requestId" />
    <button class="btn btn-sm" type="submit">Confirm Login</button>
  </form>

  <form method="POST" action="?/getScopes" use:enhance>
    <button class="btn btn-sm" type="submit">Get Scopes</button>
  </form>
</div>
