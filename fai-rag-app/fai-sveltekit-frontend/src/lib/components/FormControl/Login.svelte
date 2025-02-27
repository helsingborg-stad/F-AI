<script lang="ts">
  export let sessionId = null
</script>

<div class="card-container">
  <div class="card-body">
    <h2 class="heading">
      {#if sessionId}
        PIN
      {:else}
        Folkets Ai
      {/if}
    </h2>
    <form class="space-y-6" method="POST">
      <div class="input input-bordered input-ghost flex w-full items-center space-x-3">
        <input
          class="mt-0 max-h-full w-full max-w-full grow border-none"
          name="email"
          type="email"
          placeholder="Ange din e-post"
          required
        />
      </div>
      <button class="btn btn-neutral" type="submit">Logga in</button>
    </form>
  </div>
</div>

<style lang="postcss">
  .card-container {
    @apply card z-50 mx-auto w-full max-w-sm bg-base-100 bg-opacity-80 pt-6 shadow-2xl;
    @layer drop-shadow-4xl {
    }
  }

  .heading {
    @apply mb-6 mt-0 text-center text-4xl font-extrabold;
  }
</style>
