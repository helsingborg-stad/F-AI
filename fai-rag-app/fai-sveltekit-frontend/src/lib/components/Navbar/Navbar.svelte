<!--TODO: Remove dropdown from navbar and place it in top `+layout.page`-->

<div class="navbar bg-gray-50">
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle md:hidden">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h7" />
        </svg>
      </div>
    </div>
    <slot name="left"></slot>
  </div>
  <div class="navbar-end">
    <slot name="right"></slot>
  </div>
</div>