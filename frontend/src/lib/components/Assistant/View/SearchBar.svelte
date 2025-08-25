<script lang="ts">
  interface Props {
    value: string
  }

  let { value = $bindable() }: Props = $props()
</script>

<label class="input input-lg input-bordered m-1 flex items-center gap-2">
  <input bind:value type="text" class="grow" placeholder="Search" />
</label>
