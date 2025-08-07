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

<dialog bind:this={dialog} class="modal prose" onclick={handleBackdropClick}>
  <div class="modal-box w-11/12 h-5/6 max-w-5xl flex pt-12 justify-center items-center">
    <div class="absolute right-2 top-2 flex gap-1 justify-end">
      <a
        bind:this={downloadAnchor}
        class="hidden"
        target="_blank"
        href={href}
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
    <div class="max-w-full max-h-full shrink flex flex-col justify-center items-center">
      <img class="m-0 p-0 h-full w-full max-w-fit max-h-fit object-contain" src={href} alt={text} />
      <span>{text}</span>
    </div>
  </div>
</dialog>
