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
    export let fileSizeLimit: number | null = null;

    let ref: HTMLInputElement;
    let notification: string = '';

    onMount(() => autoFocus && (ref?.focus() !== undefined));

    function calculateTotalFilesSize(files: FileList): number {
        let size = 0;
        for (let i = 0; i < files.length; i++) {
            size += files[i].size;
        }
        return size;
    }

    const handleFileChange = (event: Event) => {
      const t = event.target as HTMLInputElement
      if (t.files && t.files.length) {
        const totalFileSize = calculateTotalFilesSize(t.files);
        const maxFileSizeInBytes = fileSizeLimit! * 1024 * 1024;
        if (totalFileSize > maxFileSizeInBytes) {
          notification = `Total file size is too large. Max file size is ${fileSizeLimit} MB`;
          t.value = '';
          t.files = null;
        } else {
          notification = '';
        }
      }
    };
</script>

{#if notification}
  <p class="alert alert-warning">{notification}</p>
{/if}

<label class:form-control={1}>
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
            on:change={fileSizeLimit ? handleFileChange : null}
    />
    {#if error}
        <div class="label label-text text-error mt-1">{error}</div>
    {/if}
</label>
