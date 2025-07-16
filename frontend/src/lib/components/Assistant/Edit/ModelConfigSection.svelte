<script lang="ts">
  import {m} from '$lib/paraglide/messages.js'
  import Section from '$lib/components/Form/Section.svelte'

  interface Props {
    canEdit: boolean;
  }

  let { canEdit }: Props = $props()
</script>

<Section title={m.assistant_edit_model_configuration_section_title()}>
  <label class="form-control w-full">
    <div class="label">
      <span class="label-text">{m.assistant_edit_model_configuration_response_format()}</span>
    </div>
    <select class="select select-bordered select-sm text-sm" disabled={!canEdit}>
      <option>text</option>
      <option>json_format</option>
    </select>
  </label>
</Section>
