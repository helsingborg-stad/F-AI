<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import DaisyButton from './DaisyButton.svelte'

  const { Story } = defineMeta({
    title: 'Example/DaisyButton',
    component: DaisyButton,
    tags: ['autodocs'],
  })
</script>

<Story name="Primary" />
