<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { action } from '@storybook/addon-actions';
  import ChatInput from '$lib/components/Chat/ChatInput.svelte';

  const { Story } = defineMeta({
    title: 'Components/Chat/ChatInput',
    component: ChatInput,
    tags: ['autodocs'],
    argTypes: {
      placeholder: {
        control: 'text',
        description: 'Placeholder text for the input field.',
      },
    },
  });
</script>

<Story
  name="Default"
  args={{
    placeholder: 'Type your message...',
  }}
  send={action('send')}
></Story>
