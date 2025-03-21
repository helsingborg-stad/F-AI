<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Login from '$lib/components/Login/Login.svelte'

  const { Story } = defineMeta({
    title: 'Components/Login',
    component: Login,
    tags: ['autodocs'],
    argTypes: {
      isIDSubmittedInitialState: { control: 'boolean' },
    },
  })
</script>

<Story name="Default" />

<Story name="Valid email" args={{ IDInitialState: 'john.doe@email.com' }} />

<Story name="Input code blank" args={{ IDInitialState: 'john.doe@email.com', isIDSubmittedInitialState: true }} />

<Story name="With OPT notification text"
       args={{
         IDInitialState: 'john.doe@email.com',
         isIDSubmittedInitialState: true,
         OTPInitialState: '1122',
         OTPMessage: 'There was an error verifying your code.'
       }}
/>