<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Login from '$lib/components/FormControl/Login.svelte'

  const { Story } = defineMeta({
    title: 'Components/Login',
    component: Login,
    tags: ['autodocs'],
    argTypes: {
      sessionId: { control: 'text' },
    },
  })
</script>

<Story
  name="Default"
  args={{
    sessionId: null,
  }}
/>

<Story
  name="Pin"
  args={{
    sessionId: '1234567890',
  }}
/>
