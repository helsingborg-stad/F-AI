<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'
  import Section from '$lib/components/Form/Section.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'

  interface Props {
    canEdit: boolean
    isPublic: boolean
  }

  let { canEdit, isPublic }: Props = $props()
</script>

<Section title={m.assistant_edit_access_section_title()}>
  <div class="mt-2 flex flex-row place-content-between items-center">
    <div class="flex flex-row gap-2">
      <input
        type="checkbox"
        name="public"
        class="toggle toggle-success toggle-sm"
        checked={isPublic}
        disabled={!canEdit}
      />
      <InfoTooltip
        toolTip="Public access allows other users to see and use, but not edit this assistant."
      >
        <div class="select-none text-sm font-medium">
          {m.assistant_edit_access_section_public()}
        </div>
      </InfoTooltip>
    </div>
  </div>
</Section>
