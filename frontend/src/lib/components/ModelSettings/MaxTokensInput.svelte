<script lang="ts">
  interface Props {
    value: number
    disabled?: boolean
    onchange?: (value: number) => void
  }

  let {
    value = $bindable(4096),
    disabled = false,
    onchange,
  }: Props = $props()

  function handleChange(event: Event) {
    const target = event.target as HTMLInputElement
    const newValue = parseInt(target.value) || 4096
    value = newValue
    onchange?.(newValue)
  }

  const commonContextWindows = [
    { value: 4096, label: '4K' },
    { value: 8192, label: '8K' },
    { value: 16384, label: '16K' },
    { value: 32768, label: '32K' },
    { value: 65536, label: '64K' },
    { value: 131072, label: '128K' },
    { value: 262144, label: '256K' },
  ]

  function setPreset(presetValue: number) {
    value = presetValue
    onchange?.(presetValue)
  }
</script>

<div class="form-control w-full">
  <label for="maxTokens" class="label">
    <span class="label-text font-medium">Max Tokens (Context Window)</span>
  </label>
  <input
    type="number"
    id="maxTokens"
    class="input input-bordered w-full"
    bind:value
    {disabled}
    onchange={handleChange}
    min="1"
    max="1000000"
    placeholder="4096"
  />
  <div class="label">
    <span class="label-text-alt text-base-content/60">
      Maximum number of tokens the model can process
    </span>
  </div>
  
  {#if !disabled}
    <div class="flex flex-wrap gap-1 mt-1">
      <span class="text-xs text-base-content/60 mr-1">Quick select:</span>
      {#each commonContextWindows as preset}
        <button
          type="button"
          class="btn btn-xs {value === preset.value ? 'btn-primary' : 'btn-ghost'}"
          onclick={() => setPreset(preset.value)}
        >
          {preset.label}
        </button>
      {/each}
    </div>
  {/if}
</div>