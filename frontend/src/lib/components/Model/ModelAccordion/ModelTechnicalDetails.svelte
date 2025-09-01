<script lang="ts">
  interface Props {
    modelKey: string
    provider: string
  }

  let { modelKey, provider }: Props = $props()
</script>

<div>
  <h4 class="mb-2 text-xs font-semibold uppercase tracking-wide text-base-content/70">
    Technical Details
  </h4>
  <div class="space-y-1 text-sm text-base-content/70">
    <div class="flex justify-between">
      <span class="font-medium">Model Key:</span>
      <code class="rounded bg-base-300 px-2 py-0.5 font-mono text-xs">{modelKey}</code>
    </div>
    <div class="flex justify-between">
      <span class="font-medium">Provider:</span>
      <span>{provider}</span>
    </div>
  </div>
</div>
