<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import InfoTooltip from '$lib/components/InfoTooltip/InfoTooltip.svelte'


  const { Story } = defineMeta({
    title: 'Components/InfoTooltip',
    component: InfoTooltip,
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={{ toolTip: 'This is a tooltip' }} />

<Story name="With text as snippet">
  <InfoTooltip toolTip="This is a tooltip">
    <div class="text-sm">Hover on me for tooltips</div>
  </InfoTooltip>
</Story>


