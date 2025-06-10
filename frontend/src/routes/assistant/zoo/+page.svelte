<script lang="ts">
  import AssistantZoo from '$lib/components/Assistant/View/AssistantZoo.svelte'

  let { data } = $props()

  const { exhibits } = data
</script>

<div class="w-full mx-auto max-w-3xl p-4 mb-32">
  <div class="mb-6">
    <div class="my-2 text-center text-3xl font-bold md:my-4 md:text-5xl">
      Assistant Zoo
    </div>
    <div class="mx-auto w-full text-center text-sm md:text-lg md:leading-tight text-gray-500">
      Discover all the different kinds of assistants hosted by Helsingborg. Don't be afraid to click on an assistant to
      read more!
    </div>
  </div>
  <AssistantZoo {exhibits} />
</div>
