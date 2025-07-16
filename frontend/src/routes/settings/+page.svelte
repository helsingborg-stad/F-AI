<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
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
    <h1>{m.settings_page_title()}</h1>
    <p>{m.settings_page_description()}</p>
    <form method="POST" action="?/update">
      <h2 class="mt-12">{m.settings_basic_section_heading()}</h2>
      <TextInput
        name="fixedOptCode"
        label={m.settings_basic_fixed_pin_label()}
        value={backendSettings.fixedOptCode}
      />
      <h2 class="mt-12">{m.settings_ai_section_heading()}</h2>
      <TextInput
        name="openAiApiKey"
        label={m.settings_openai_api_key_label()}
        value={backendSettings.openAiApiKey}
      />
      <TextInput
        name="anthropicApiKey"
        label={m.settings_anthropic_api_key_label()}
        value={backendSettings.anthropicApiKey}
      />
      <TextInput
        name="mistralApiKey"
        label={m.settings_mistral_api_key_label()}
        value={backendSettings.mistralApiKey}
      />
      <h2 class="mt-12">{m.settings_email_section_heading()}</h2>
      <TextInput
        name="brevoApiUrl"
        label={m.settings_brevo_api_url_label()}
        value={backendSettings.brevoApiUrl}
        placeholder=""
      />
      <TextInput
        name="brevoApiKey"
        label={m.settings_brevo_api_key_label()}
        value={backendSettings.brevoApiKey}
        placeholder="xkeysib-..."
      />
      <button type="submit" class="btn btn-sm btn-primary mt-16">{m.common_action_save()}</button>
    </form>
  </div>
</div>
