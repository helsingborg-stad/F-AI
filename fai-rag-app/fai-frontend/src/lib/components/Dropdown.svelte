<script lang="ts">
    import {onMount} from 'svelte';

    export let title: string = 'Dropdown';
    export let position: 'top' | 'bottom' | 'left' | 'right' = 'bottom';
    export let openOnHover: boolean = false;
    export let className: string | null;
    export {className as class};
    export let buttonClass: string = 'btn';
    export let contentClass: string = '';

    let isOpen = false;

    // Function to toggle dropdown state
    function toggleDropdown() {
        isOpen = !isOpen;
    }

    let isDropdownOpen = false // default state (dropdown close)

    const handleDropdownClick = () => {
        isDropdownOpen = !isDropdownOpen // togle state on click
    }

    const handleDropdownFocusLoss = ({relatedTarget, currentTarget}) => {
        // use "focusout" event to ensure that we can close the dropdown when clicking outside or when we leave the dropdown with the "Tab" button
        if (relatedTarget instanceof HTMLElement && currentTarget.contains(relatedTarget)) return // check if the new focus target doesn't present in the dropdown tree (exclude ul\li padding area because relatedTarget, in this case, will be null)
        isDropdownOpen = false
    }
    // Accessibility and other initializations
    onMount(() => {
        // Initialization code here
    });
</script>

<section on:focusout={handleDropdownFocusLoss}
         class={`dropdown ${position} ${openOnHover ? 'dropdown-hover' : ''} ${className}`}>
    <button
            on:click={handleDropdownClick} class={`${buttonClass}`} aria-haspopup="true"
            aria-expanded={isDropdownOpen}>
        <slot name="title" title={title}>{title}</slot>
    </button>
    {#if isDropdownOpen}
        <div class={`${contentClass} dropdown-content`}>
            <slot></slot>
        </div>
    {/if}
</section>