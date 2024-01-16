<script lang="ts">
    let className: string | null = null;

    export let name: string;
    export let title: string | null = null;
    export let placeholder: string | null = null;
    export let required: boolean | null = null;
    export let html_type: 'text' | 'password' | 'hidden' | 'number' | 'email' | 'tel' = 'text';
    export let value: string | null = null;
    export let hidden: boolean = false;

    export {className as class};

    const props = {
        ...{class: 'input w-full' + (className ? (' ' + className) : '')},
        ...(title ? {title} : {}),
        ...(placeholder ? {placeholder} : {}),
        ...(required !== null ? {required} : {}),
        ...(value !== null ? {value: value} : {}),
        ...(html_type !== 'text' ? {type: html_type} : {}),
        ...(hidden ? {hidden} : {})
    }
</script>

<input {name} {...props}/>
