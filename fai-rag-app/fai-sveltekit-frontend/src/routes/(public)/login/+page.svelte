<script lang="ts">
  import Login from '$lib/components/FormControl/Login.svelte'
  let sessionId = null
</script>

<svelte:head>
  <title>Folkets Ai - Logga in</title>
</svelte:head>

<div class="page-container">
  <Login {sessionId} />
</div>

<style lang="postcss">
  .page-container {
    @apply flex h-screen items-center justify-center border-4 border-neutral border-opacity-25;
    background-image: url("data:image/svg+xml,%3Csvg width=\'6\' height=\'6\' viewBox=\'0 0 6 6\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'0.31\' fill-rule=\'evenodd\'%3E%3Cpath d=\'M5 0h1L0 6V5zM6 5v1H5z\'/%3E%3C/g%3E%3C/svg%3E");
  }
</style>
