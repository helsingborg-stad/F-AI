<script lang="ts">
    import {onMount} from 'svelte'

    export let name: string
    export let title: string | null = null
    export let error: string | null = null
    export let placeholder: string | null = null;
    export let required: boolean | null = null;
    export let id: string = name;
    export let className: string | null = null;
    export {className as class};
    export let value: string | null = null;
    export let block: boolean | null = true;
    export let variant: 'ghost' | 'bordered' = 'bordered'
    export let autoFocus: boolean | null = null;
    export let multiple: boolean | null = null;

    let ref: HTMLInputElement;
    let notification: string = '';
    const FILE_SIZE_LIMIT = 10; // MB

    onMount(() => autoFocus && (ref?.focus() !== undefined));

    function calculateTotalFilesSize(files: FileList): { totalFiles: number, totalFileSize: number } {
        const totalFiles = files.length;
        let totalFileSize = 0;

        for (let i = 0; i < totalFiles; i++) {
            totalFileSize += files[i].size;
        }

        return { totalFiles, totalFileSize };
    }

    const handleFileChange = (event: Event) => {
      const t = event.target as HTMLInputElement
      if (t.files && t.files.length) {
        const { totalFiles, totalFileSize } = calculateTotalFilesSize(t.files);
        const maxFileSizeInBytes = FILE_SIZE_LIMIT * 1024 * 1024;
        if (totalFileSize > maxFileSizeInBytes) {
          notification = `Total file size is too large. Max file size is ${FILE_SIZE_LIMIT} MB`;
          t.value = '';
          t.files = null;
        } else {
          notification = '';
        }
        console.log(`Total Files: ${totalFiles}`);
        console.log(`Total File Size: ${totalFileSize} bytes`);
      }
    };
</script>

<style>
  .notification {
    background-color: #ffcccc;
    border: 1px solid #ff0000;
    color: #ff0000;
    border-radius: 5px;
    margin: 1rem;
    padding: 1rem;
}
</style>

<label class:form-control={1}>
    {#if notification}
      <div class="notification">{notification}</div>
    {/if}
    <input
            bind:this={ref}
            class:file-input={1}
            class:file-input-error={error}
            class:file-input-bordered={variant === 'bordered'}
            class:file-input-ghost={variant === 'ghost'}
            class:w-full={block}
            class={className ?? null}
            type='file'
            multiple={multiple}
            required={required}
            {name}
            {id}
            {title}
            {placeholder}
            {value}
            on:change={handleFileChange}
    />
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</label>
