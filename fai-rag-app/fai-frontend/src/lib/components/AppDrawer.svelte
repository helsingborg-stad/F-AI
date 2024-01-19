<script></script>

<div {...$$props?.slot ? {slot: $$props.slot} : {}} class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
    <div class="w-80 h-screen"></div>
    <aside class=" bg-base-200 min-h-screen w-80 fixed z-50 left-0 top-0 border-r border-neutral shadow">
        <slot/>
    </aside>
</div>