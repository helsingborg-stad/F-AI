<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    text: string
    href: string
  }

  const { text, href }: Props = $props()
  let dialog: HTMLDialogElement | null = $state(null)
  let downloadAnchor: HTMLAnchorElement | null = $state(null)

  function handleClick() {
    dialog?.showModal()
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === dialog) {
      dialog?.close()
    }
  }

  function handleDownload() {
    downloadAnchor?.click()
  }
</script>

<button class="bg-amber-600" onclick={handleClick}>
  <img class="m-0 max-w-96" src={href} alt={text} />
</button>

<dialog bind:this={dialog} class="prose modal" onclick={handleBackdropClick}>
  <div class="modal-box flex h-5/6 w-11/12 max-w-5xl items-center justify-center pt-12">
    <div class="absolute right-2 top-2 flex justify-end gap-1">
      <a
        bind:this={downloadAnchor}
        class="hidden"
        target="_blank"
        {href}
        download
        aria-label="hidden downloader anchor"
      ></a>
      <button class="btn btn-circle btn-ghost btn-sm" onclick={handleDownload}>
        <Icon icon={icons['download']} width={16} height={16} />
      </button>
      <form method="dialog">
        <button class="btn btn-circle btn-ghost btn-sm">✕</button>
      </form>
    </div>
    <div class="flex max-h-full max-w-full shrink flex-col items-center justify-center">
      <img
        class="m-0 h-full max-h-fit w-full max-w-fit object-contain p-0"
        src={href}
        alt={text}
      />
      <span>{text}</span>
    </div>
  </div>
</dialog>
