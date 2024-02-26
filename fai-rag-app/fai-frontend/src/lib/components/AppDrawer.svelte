<script></script>

<div
        {...$$props?.slot ? {slot: $$props.slot} : {}}
        class="drawer-side z-40"
        style="scroll-behavior: smooth; scroll-padding-top: 5rem;">
    <label
            for="my-drawer-2"
            aria-label="close sidebar"
            class="drawer-overlay"></label>
    <aside
            class="bg-base-100 min-h-screen w-80  border-r  border-neutral border-opacity-25 shadow">
        <slot/>
    </aside>
</div>