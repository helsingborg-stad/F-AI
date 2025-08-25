<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    link: string
  }

  const { link }: Props = $props()

  const defaultCopyText = 'Copy link'
  let copyText = $state(defaultCopyText)

  async function onClick() {
    try {
      await navigator.clipboard.writeText(window.location.origin + link)
      copyText = 'Link copied!'
    } catch (err) {
      console.error('Failed to copy link:', err)
    }
  }
</script>

<div class="tooltip z-40" data-tip={copyText}>
  <button
    type="submit"
    class="btn btn-circle btn-ghost btn-sm"
    onclick={onClick}
    onmouseenter={() => (copyText = defaultCopyText)}
  >
    <Icon icon={icons['share']} width={20} height={20} />
  </button>
</div>
