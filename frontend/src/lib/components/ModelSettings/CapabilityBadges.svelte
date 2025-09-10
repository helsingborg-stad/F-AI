<script lang="ts">
  import Badge from '$lib/components/Badge/Badge.svelte'

  interface Capabilities {
    supportsImages?: boolean
    supportsReasoning?: boolean
    supportsCodeExecution?: boolean
    supportsFunctionCalling?: boolean
    supportsWebSearch?: boolean
    maxTokens?: number
  }

  interface Props {
    capabilities?: Capabilities
  }

  let { capabilities }: Props = $props()
</script>

{#if capabilities}
  <div class="mt-2 flex flex-wrap gap-2">
    {#if capabilities.supportsImages}
      <Badge type="image" size="sm" label="Image Processing" />
    {/if}
    {#if capabilities.supportsReasoning}
      <Badge type="reasoning" size="sm" label="Advanced Reasoning" />
    {/if}
    {#if capabilities.supportsFunctionCalling}
      <Badge type="function-calling" size="sm" />
    {/if}
    {#if capabilities.supportsWebSearch}
      <Badge type="web-search" size="sm" label="Web Search" />
    {/if}
    {#if capabilities.maxTokens && capabilities.maxTokens > 4096}
      <Badge type="tokens" size="sm" value={capabilities.maxTokens} />
    {/if}
  </div>
{/if}
