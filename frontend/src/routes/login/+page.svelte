<script lang="ts">
  import Login from '$lib/components/Login/Login.svelte'

  let { form } = $props()
</script>

<div class="min-h-screen bg-base-200 flex items-center justify-center p-4">
  <Login form={form} />
</div>