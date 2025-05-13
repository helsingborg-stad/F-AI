<script lang="ts">
  import TextInput from '$lib/components/FormControl/TextInput.svelte'
  import type { IApiSettings } from '$lib/types.js'

  let { data } = $props<{ settings: IApiSettings }>()

  const backendSettings = data.settings
</script>

<div
  class="flex-1 overflow-auto"
  style="max-height: calc(100vh - 64px);"
>
  <div class="p-4">
    <h1>Settings</h1>
    <p>Configure your API settings here.</p>
    <form method="POST" action="?/update">
      <h2 class="mt-12">Basic</h2>
      <TextInput
        name="fixedOptCode"
        label="Fixed pin"
        value={backendSettings.fixedOptCode}
      />
      <h2 class="mt-12">AI Settings</h2>
      <TextInput
        name="openAiApiKey"
        label="OpenAI API key"
        value={backendSettings.openAiApiKey}
      />
      <TextInput
        name="anthropicApiKey"
        label="Anthropic API key"
        value={backendSettings.anthropicApiKey}
      />
      <TextInput
        name="mistralApiKey"
        label="Mistral API key"
        value={backendSettings.mistralApiKey}
      />
      <h2 class="mt-12">E-mail (Brevo)</h2>
      <TextInput
        name="brevoApiUrl"
        label="Brevo API URL"
        value={backendSettings.brevoApiUrl}
        placeholder=""
      />
      <TextInput
        name="brevoApiKey"
        label="Brevo API Key"
        value={backendSettings.brevoApiKey}
        placeholder="xkeysib-..."
      />
      <button type="submit" class="btn btn-sm btn-primary mt-16">Save settings</button>
    </form>
  </div>
</div>