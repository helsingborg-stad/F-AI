<script lang="ts">
  import Section from '$lib/components/Form/Section.svelte'
  import CapabilityToggle from './CapabilityToggle.svelte'
  import MaxTokensInput from './MaxTokensInput.svelte'

  interface Capabilities {
    supportsImages: boolean
    supportsReasoning: boolean
    supportsCodeExecution: boolean
    supportsFunctionCalling: boolean
    supportsWebSearch: boolean
    maxTokens: number
  }

  interface Props {
    capabilities: Capabilities
    disabled?: boolean
  }

  let {
    capabilities = $bindable({
      supportsImages: false,
      supportsReasoning: false,
      supportsCodeExecution: false,
      supportsFunctionCalling: true,
      supportsWebSearch: false,
      maxTokens: 4096,
    }),
    disabled = false,
  }: Props = $props()

  const capabilityDescriptions = {
    images: "Model can process and understand image inputs",
    reasoning: "Model supports advanced reasoning and chain-of-thought",
    codeExecution: "Model can execute code and run computations",
    functionCalling: "Model supports function/tool calling for API interactions",
    webSearch: "Model can search the web to access up-to-date information",
  }
</script>

<Section title="Model Capabilities">
  <div class="space-y-3">
    <CapabilityToggle
      label="Supports Reasoning"
      description={capabilityDescriptions.reasoning}
      bind:checked={capabilities.supportsReasoning}
      {disabled}
    />
    
    <CapabilityToggle
      label="Supports Web Search"
      description={capabilityDescriptions.webSearch}
      bind:checked={capabilities.supportsWebSearch}
      {disabled}
    />
    <div class="pt-2">
      <MaxTokensInput
        bind:value={capabilities.maxTokens}
        {disabled}
      />
    </div>
  </div>
</Section>
