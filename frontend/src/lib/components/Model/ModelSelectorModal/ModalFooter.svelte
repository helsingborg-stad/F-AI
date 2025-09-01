<script lang="ts">
  interface Props {
    onCancel: () => void
    onConfirm: () => void
    confirmDisabled?: boolean
    cancelText?: string
    confirmText?: string
  }

  let {
    onCancel,
    onConfirm,
    confirmDisabled = false,
    cancelText = 'Cancel',
    confirmText = 'Select Model'
  }: Props = $props()
</script>

<div class="sticky bottom-0 z-10 bg-base-100 border-t border-base-300 pt-4 mt-4">
  <div class="flex justify-end gap-2">
    <button
      type="button"
      class="btn btn-ghost btn-sm"
      onclick={onCancel}
    >
      {cancelText}
    </button>
    <button
      type="button"
      class="btn btn-primary btn-sm"
      onclick={onConfirm}
      disabled={confirmDisabled}
    >
      {confirmText}
    </button>
  </div>
</div>
