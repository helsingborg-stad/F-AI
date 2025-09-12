<script lang="ts">
  import { m } from '$lib/paraglide/messages.js'

  interface Props {
    title?: string
    description?: string
    canCreate?: boolean
    onCreateClick?: () => void
  }

  let {
    title = m.settings_models_label(),
    description = 'Manage AI models available for assistants and conversations.',
    canCreate = false,
    onCreateClick,
  }: Props = $props()
</script>

<header class="mb-6">
  <h1 class="mb-2 text-3xl font-bold text-base-content">
    {title}
  </h1>
  <p class="text-base-content/70">
    {description}
  </p>
</header>

{#if canCreate && onCreateClick}
  <div class="mb-6">
    <button type="button" class="btn btn-primary btn-sm" onclick={onCreateClick}>
      <span class="text-sm">+ Create Model</span>
    </button>
  </div>
{/if}
