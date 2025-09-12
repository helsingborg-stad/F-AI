<script lang="ts">
  interface Props {
    label: string
    description?: string
    checked: boolean
    disabled?: boolean
    onchange?: (checked: boolean) => void
  }

  let {
    label,
    description,
    checked = $bindable(),
    disabled = false,
    onchange,
  }: Props = $props()

  function handleChange(event: Event) {
    const target = event.target as HTMLInputElement
    checked = target.checked
    onchange?.(target.checked)
  }
</script>

<label class="form-control">
  <div class="label cursor-pointer justify-start space-x-3">
    <input
      type="checkbox"
      class="checkbox checkbox-primary"
      bind:checked
      {disabled}
      onchange={handleChange}
    />
    <div class="flex-1">
      <span class="label-text font-medium">{label}</span>
      {#if description}
        <p class="text-xs text-base-content/60 mt-0.5">{description}</p>
      {/if}
    </div>
  </div>
</label>
