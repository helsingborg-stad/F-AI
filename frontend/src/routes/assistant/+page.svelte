<script lang="ts">
  import type { IAssistant } from '$lib/types.js'

  let { data } = $props<{ assistants: IAssistant[] }>()

  const assistants = data.assistants
  const nrOfAssistants = assistants.length
</script>
<div class="px-8">
  <div class="py-4 flex flex-col">
    <div class="flex">
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
    {#each assistants as assistant}
      <div class="card card-compact bg-base-100 w-96 shadow-xl">
        <figure>
          <img
            src="https://img.daisyui.com/images/stock/photo-1494232410401-ad00d5433cfa.webp"
            alt={assistant.name} />
        </figure>
        <div class="card-body">
          <h2 class="card-title">{assistant.name}</h2>
          <p>{assistant.description}</p>
          <div class="card-actions justify-end">
            <a href="assistant/details?assistant_id={assistant.id}" class="btn btn-primary">Details</a>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
