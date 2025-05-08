<script>
  import Section from '$lib/components/Form/Section.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'

  let { canEdit } = $props()
</script>

<Section title={"Access"}>
  <div class="flex flex-row place-content-between items-center mt-2">
    <div class="flex flex-row gap-2">
      <input type="checkbox" name="public" class="toggle toggle-sm toggle-success" disabled={!canEdit} />
      <InfoTooltip
        toolTip="Public access allows other users to see and use, but not edit this assistant.">
        <div class="text-sm font-medium select-none">Public</div>
      </InfoTooltip>
    </div>
  </div>
</Section>