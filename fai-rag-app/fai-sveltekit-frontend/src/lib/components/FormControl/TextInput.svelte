<script lang="ts">
	export let placeholder: string = '';
	export let label: string = '';
	export let value: string | null = null;
	export let required: boolean = false;
</script>

<label class="form-control w-full max-w-lg mb-4 last:mb-0">
	<div class="label">
		<span class="label-text">{label}</span>
		{#if required}
			<span class="text-red-700 label-text-alt">Required</span>
		{/if}
	</div>
	<input bind:value={value} {placeholder} type="text" class="input input-bordered w-full max-w-lg">
</label>
