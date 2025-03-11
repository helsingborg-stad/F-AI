<script>
  let { children } = $props()
</script>

<div class="flex flex-grow bg-base-200">
  <main class="m-2 flex-grow rounded-lg border bg-stone-50">
    {@render children()}
  </main>
</div>
