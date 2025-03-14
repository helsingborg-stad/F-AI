<script lang="ts">
	import avatarPlaceholder from '$lib/assets/fai-avatar.png';

  export let avatarSrc: string = avatarPlaceholder;
</script>

<div class="relative w-56 self-center">

	<div class="avatar">
	<div class="rounded">
	    <img src={avatarSrc} alt="Avatar" />
	</div>
</div>

	<div class="absolute bottom-4 right-4">
		<button class="btn btn-circle">
  		<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image-up"><path d="M10.3 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10l-3.1-3.1a2 2 0 0 0-2.814.014L6 21"/><path d="m14 19.5 3-3 3 3"/><path d="M17 22v-5.5"/><circle cx="9" cy="9" r="2"/></svg>
		</button>
	</div>
</div>