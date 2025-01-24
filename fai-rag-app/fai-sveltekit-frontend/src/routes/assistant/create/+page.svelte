<script>
	import SetAssistantAvatar from '$lib/components/assistant/SetAssistantAvatar.svelte';
</script>

<p>Create new assistant</p>
<div class="flex w-full justify-between p-4 gap-2">
	<SetAssistantAvatar />
	<div class="basis-5/6">
		<div class="flex flex-col w-full justify-between gap-4">
			<form method="POST" action="?/create">
				<div class="flex flex-col w-full justify-between gap-2">
					<label class="form-control w-full max-w-xs">
						<div class="label">
							<span class="label-text">Assistant name</span>
						</div>
						<input
							class="input input-sm input-bordered w-full max-w-xs"
							name="name"
							type="text"
							autocomplete="off"
							required
						/>
					</label>
					<select
						class="select select-sm select-bordered w-full max-w-xs"
						name="model"
						required
					>
						<option disabled selected>Select a model</option>
						<option>o1</option>
						<option>GPT-4</option>
					</select>
					<label class="form-control">
						<div class="label">
							<span class="label-text">System prompt</span>
						</div>
						<textarea
							class="textarea textarea-bordered h-24"
							name="instructions"
						></textarea>
					</label>
					<button class="btn">Create assistant</button>
				</div>
			</form>
		</div>
	</div>
</div>
