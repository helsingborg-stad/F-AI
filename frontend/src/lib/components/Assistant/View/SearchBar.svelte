<script lang="ts">
  interface Props {
    value: string
  }

  let { value = $bindable() }: Props = $props()
</script>

<label class="input input-bordered input-lg flex items-center gap-2 m-1">
  <input bind:value type="text" class="grow" placeholder="Search" />
</label>