<script lang="ts">
  import { icons } from '$lib/components/Icon/icons.js'
  import Icon from '$lib/components/Icon/Icon.svelte'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'
  import Section from '$lib/components/Form/Section.svelte'
  import HorizontalDivider from '$lib/components/Divider/HorizontalDivider.svelte'

  interface Props {
    canEdit: boolean;
  }

  let { canEdit }: Props = $props()
</script>

<Section title={"Tools"}>
  <div class="flex flex-row place-content-between items-center mt-2">
    <div class="flex flex-row gap-2">
      <input type="checkbox" class="toggle toggle-sm toggle-success" disabled={!canEdit} />
      <InfoTooltip
        toolTip="File Search enables the assistant with knowledge from files that you or your users upload.">
        <div class="text-sm font-medium select-none">File search</div>
      </InfoTooltip>
    </div>
    <div>
      <button class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons["settings"]} width={16} height={16} />
      </button>
      <button class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons["plus"]} width={16} height={16} />
        <span class="text-s">Files</span>
      </button>
    </div>
  </div>
  <HorizontalDivider />
  <div class="flex flex-row place-content-between items-center">
    <div>
      <InfoTooltip
        toolTip="Function calling lets you describe custom functions of your app or external APIs to the assistant.">
        <div class="text-sm font-medium select-none">Functions</div>
      </InfoTooltip>
    </div>
    <div>
      <button class="btn btn-sm" disabled={!canEdit}>
        <Icon icon={icons["plus"]} width={16} height={16} />
        <span class="text-s">Functions</span>
      </button>
    </div>
  </div>
</Section>