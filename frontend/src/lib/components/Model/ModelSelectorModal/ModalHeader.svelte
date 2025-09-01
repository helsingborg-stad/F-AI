<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'

  interface Props {
    title?: string
    subtitle?: string
  }

  let {
    title = m.assistant_edit_model_placeholder(),
    subtitle = 'Choose the AI model for your assistant'
  }: Props = $props()
</script>

<div class="sticky top-0 z-10 bg-base-100 border-b border-base-300 pb-4 mb-4">
  <h3 class="text-lg font-bold">{title}</h3>
  <p class="text-sm text-base-content/70 mt-1">
    {subtitle}
  </p>
</div>
