<script lang="ts">
  import {m } from '$lib/paraglide/messages.js'
  import AssistantZoo from '$lib/components/Assistant/View/AssistantZoo.svelte'

  let { data } = $props()

  const { exhibits } = data
</script>

<div class="w-full mx-auto max-w-3xl p-4 mb-32">
  <div class="mb-6">
    <div class="my-2 text-center text-3xl font-bold md:my-4 md:text-5xl">
      {m.assistant_zoo_page_title()}
    </div>
    <div class="mx-auto w-full text-center text-sm md:text-lg md:leading-tight text-gray-500">
      {m.assistant_zoo_page_description()}
    </div>
  </div>
  <AssistantZoo {exhibits} />
</div>
