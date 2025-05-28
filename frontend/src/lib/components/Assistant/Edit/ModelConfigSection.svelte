<script lang="ts">
  import Section from '$lib/components/Form/Section.svelte'

  interface Props {
    canEdit: boolean;
  }

  let { canEdit }: Props = $props()
</script>

<Section title={"Model configuration"}>
  <label class="form-control w-full">
    <div class="label">
      <span class="label-text">Response format</span>
    </div>
    <select class="select select-bordered select-sm text-sm" disabled={!canEdit}>
      <option>text</option>
      <option>json_format</option>
    </select>
  </label>
</Section>