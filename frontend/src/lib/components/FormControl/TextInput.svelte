<script lang="ts">
  export let placeholder: string = ''
  export let label: string = ''
  export let value: string | null = null
  export let required: boolean = false
  export let name: string = ''
</script>

<label class="form-control mb-4 w-full max-w-lg last:mb-0">
  <div class="label">
    <span class="label-text">{label}</span>
    {#if required}
      <span class="label-text-alt text-red-700">Required</span>
    {/if}
  </div>
  <input
    type="text"
    autocomplete="off"
    {name}
    bind:value
    {placeholder}
    class="input input-bordered w-full max-w-lg"
  />
</label>
