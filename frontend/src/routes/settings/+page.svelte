<script lang="ts">
  import TextInput from '$lib/components/FormControl/TextInput.svelte'
  import type { IApiSettings } from '$lib/types.js'

  let { data } = $props<{ settings: IApiSettings }>()

  const backendSettings = data.settings
</script>

<div class="p-4">
  <h1>Settings</h1>
  <p>Configure your API settings here.</p>
  <form method="POST" action="?/update">
    <h2 class="mt-12">Basic</h2>
    <TextInput
      label="Fixed pin" value={backendSettings.fixedOptCode}
      placeholder="NOTE: Make sure Brevo API is setup correctly to avoid account lock-out!" />
    <h2 class="mt-12">AI Settings</h2>
    <TextInput
      label="OpenAI API Key" value={backendSettings.openAiApiKey}
      placeholder="sk-proj-..." />
    <h2 class="mt-12">E-mail (Brevo)</h2>
    <TextInput
      label="Brevo API URL" value={backendSettings.brevoApiUrl}
      placeholder="" />
    <TextInput
      label="Brevo API Key" value={backendSettings.brevoApiKey}
      placeholder="xkeysib-..." />
    <button type="submit" class="btn btn-sm btn-primary mt-16">Save settings</button>
  </form>
</div>
