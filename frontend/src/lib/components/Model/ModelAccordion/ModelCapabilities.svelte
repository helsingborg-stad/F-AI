<script lang="ts">
  import Badge from '$lib/components/Badge/Badge.svelte'
  
  interface Capabilities {
    supportsImages?: boolean
    supportsReasoning?: boolean
    supportsFunctionCalling?: boolean
    maxTokens?: number
  }

  interface Props {
    capabilities?: Capabilities
  }

  let { capabilities }: Props = $props()
</script>

{#if capabilities}
  <div class="mb-4">
    <h4 class="mb-2 text-xs font-semibold uppercase tracking-wide text-base-content/70">
      Capabilities
    </h4>
    <div class="flex flex-wrap gap-2">
      {#if capabilities.supportsImages}
        <Badge type="image" size="sm" label="Image Processing" />
      {/if}
      {#if capabilities.supportsReasoning}
        <Badge type="reasoning" size="sm" label="Advanced Reasoning" />
      {/if}
      {#if capabilities.supportsFunctionCalling}
        <Badge type="function-calling" size="sm" />
      {/if}
      {#if capabilities.maxTokens && capabilities.maxTokens > 4096}
        <Badge type="tokens" size="sm" value={capabilities.maxTokens} />
      {/if}
    </div>
  </div>
{/if}
