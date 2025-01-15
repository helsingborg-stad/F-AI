<script>
	let nrOfAssistants = $state(0)
</script>
<div>
		<div class="p-5 flex flex-col">
		<div class="flex w-screen">
			Assistants
			<div class="divider divider-horizontal"></div>
			{nrOfAssistants}
		</div>
	</div>
	<div class="flex flex-wrap gap-4">
		<div class="card card-compact bg-base-100 w-96 shadow-xl">
				<figure>
					<img
						src="https://img.daisyui.com/images/stock/photo-1494232410401-ad00d5433cfa.webp"
						alt="Empty tape" />
				</figure>
				<div class="card-body">
					<h2 class="card-title">Empty tape</h2>
					<p>Create your very own assistant!</p>
					<div class="card-actions justify-end">
						<a href="assistant/create" class="btn btn-primary">Create</a>
					</div>
				</div>
			</div>
	</div>
</div>